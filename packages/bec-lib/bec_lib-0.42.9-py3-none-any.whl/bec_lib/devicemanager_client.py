import functools
import time
import traceback
import uuid
from typing import Any

from bec_lib import messages
from bec_lib.devicemanager import Device, DeviceManagerBase, Status
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger


class ScanRequestError(Exception):
    """Exception raised when a scan request is rejected."""


class RPCError(Exception):
    """Exception raised when an RPC call fails."""


logger = bec_logger.logger


def rpc(fcn):
    """Decorator to perform rpc calls."""

    @functools.wraps(fcn)
    def wrapper(self, *args, **kwargs):
        # pylint: disable=protected-access
        device, func_call = self._get_rpc_func_name(fcn=fcn)

        if kwargs.get("cached", False):
            return fcn(self, *args, **kwargs)
        return self._run_rpc_call(device, func_call, *args, **kwargs)

    return wrapper


class RPCBase:
    """
    The RPCBase class is the base class for all devices that are controlled via
    the DeviceManager. It provides a simple interface to perform RPC calls on the
    device. The RPCBase class is not meant to be used directly, but rather to be subclassed.
    """

    def __init__(self, name: str, info: dict = None, parent=None) -> None:
        """
        Args:
            name (str): The name of the device.
            info (dict, optional): The device info dictionary. Defaults to None.
            parent ([type], optional): The parent object. Defaults to None.
        """
        self.name = name
        self._config = None
        if info is None:
            info = {}
        self._info = info.get("device_info", {})
        self.parent = parent
        self._custom_rpc_methods = {}
        if self._info:
            self._parse_info()

        # the following lambda is needed to support customized RPC methods with
        # doc strings and function signatures.
        # pylint: disable=unnecessary-lambda
        self.run = lambda *args, **kwargs: self._run(*args, **kwargs)

    def _run(self, *args, **kwargs):
        device, func_call = self._get_rpc_func_name(fcn_name=self.name, use_parent=True)
        return self._run_rpc_call(device, func_call, *args, **kwargs)

    @property
    def _hints(self):
        hints = self._info.get("hints")
        if not hints:
            return []
        return hints.get("fields", [])

    @property
    def root(self):
        """Returns the root object of the device tree."""
        parent = self
        while not isinstance(parent.parent, DMClient):
            parent = parent.parent
        return parent

    def _prepare_rpc_msg(
        self, rpc_id: str, request_id: str, device: str, func_call: str, *args, **kwargs
    ) -> messages.ScanQueueMessage:
        """
        Prepares an RPC message.

        Args:
            rpc_id (str): The RPC ID.
            request_id (str): The request ID.
            device (str): The device name.
            func_call (str): The function call.
            *args: The function arguments.
            **kwargs: The function keyword arguments.

        Returns:
            messages.ScanQueueMessage: The RPC message.
        """

        params = {
            "device": device,
            "rpc_id": rpc_id,
            "func": func_call,
            "args": args,
            "kwargs": kwargs,
        }
        msg = messages.ScanQueueMessage(
            scan_type="device_rpc",
            parameter=params,
            queue="primary",
            metadata={"RID": request_id, "response": True},
        )
        return msg

    def _handle_rpc_response(self, msg: messages.DeviceRPCMessage) -> Any:
        if not msg.content["success"]:
            error = msg.content["out"]
            if not isinstance(error, dict):
                error = {"error": "Exception", "msg": error, "traceback": ""}
            raise RPCError(
                f"During an RPC, the following error occured:\n{error['error']}:"
                f" {error['msg']}.\nTraceback: {error['traceback']}\n The scan will be aborted."
            )
        if msg.content.get("out"):
            print(msg.content.get("out"))
        return_val = msg.content.get("return_val")
        if not isinstance(return_val, dict):
            return return_val
        if return_val.get("type") == "status" and return_val.get("RID"):
            return Status(self.root.parent.producer, return_val.get("RID"))
        return return_val

    def _get_rpc_response(self, request_id, rpc_id) -> Any:
        queue = self.root.parent.parent.queue
        while queue.request_storage.find_request_by_ID(request_id) is None:
            time.sleep(0.1)
        scan_queue_request = queue.request_storage.find_request_by_ID(request_id)
        while scan_queue_request.decision_pending:
            time.sleep(0.1)
        if not all(scan_queue_request.accepted):
            raise ScanRequestError(
                "Function call was rejected by the server:"
                f" {scan_queue_request.response.content['message']}"
            )
        while True:
            msg = self.root.parent.producer.get(MessageEndpoints.device_rpc(rpc_id))
            if msg:
                break
            time.sleep(0.01)
        msg = messages.DeviceRPCMessage.loads(msg)

        return self._handle_rpc_response(msg)

    def _run_rpc_call(self, device, func_call, *args, **kwargs) -> Any:
        """
        Runs an RPC call on the device. This method is used internally by the RPC decorator.
        If a call is interrupted by the user, the a stop signal is sent to this device.

        Args:
            device (str): The device name.
            func_call (str): The function call.
            *args: The function arguments.
            **kwargs: The function keyword arguments.

        Returns:
            Any: The return value of the RPC call.
        """
        try:
            # prepare RPC message
            rpc_id = str(uuid.uuid4())
            request_id = str(uuid.uuid4())
            msg = self._prepare_rpc_msg(rpc_id, request_id, device, func_call, *args, **kwargs)

            # send RPC message
            self.root.parent.producer.send(MessageEndpoints.scan_queue_request(), msg.dumps())

            # wait for RPC response
            return_val = self._get_rpc_response(request_id, rpc_id)
        except KeyboardInterrupt as exc:
            self.root.stop()
            raise RPCError("User interruption during RPC call.") from exc

        return return_val

    def _get_rpc_func_name(self, fcn_name=None, fcn=None, use_parent=False):
        if not fcn_name:
            fcn_name = fcn.__name__
        full_func_call = ".".join([self._compile_function_path(use_parent=use_parent), fcn_name])
        device = full_func_call.split(".", maxsplit=1)[0]
        func_call = ".".join(full_func_call.split(".")[1:])
        return (device, func_call)

    def _compile_function_path(self, use_parent=False) -> str:
        if use_parent:
            parent = self.parent
        else:
            parent = self
        func_call = []
        while not isinstance(parent, DMClient):
            func_call.append(parent.name)
            parent = parent.parent
        return ".".join(func_call[::-1])

    def _parse_info(self):
        if self._info.get("signals"):
            for signal_name in self._info.get("signals"):
                setattr(self, signal_name, Signal(signal_name, parent=self))
                precision = (
                    self._info.get("describe", {})
                    .get(f"{self.name}_{signal_name}", {})
                    .get("precision")
                )
                if precision is not None:
                    getattr(self, signal_name).precision = precision
        precision = self._info.get("describe", {}).get(self.name, {}).get("precision")
        if precision is not None:
            self.precision = precision
        if self._info.get("sub_devices"):
            for dev in self._info.get("sub_devices"):
                base_class = dev["device_info"].get("device_base_class")
                if base_class == "positioner":
                    setattr(
                        self,
                        dev.get("device_attr_name"),
                        Positioner(dev.get("device_attr_name"), info=dev, parent=self),
                    )
                elif base_class == "device":
                    setattr(
                        self,
                        dev.get("device_attr_name"),
                        DeviceBase(dev.get("device_attr_name"), info=dev, parent=self),
                    )

        for user_access_name, descr in self._info.get("custom_user_access", {}).items():
            if "type" in descr:
                self._custom_rpc_methods[user_access_name] = RPCBase(
                    name=user_access_name, info=descr, parent=self
                )
                setattr(
                    self,
                    user_access_name,
                    self._custom_rpc_methods[user_access_name].run,
                )
                setattr(getattr(self, user_access_name), "__doc__", descr.get("doc"))
            else:
                self._custom_rpc_methods[user_access_name] = RPCBase(
                    name=user_access_name,
                    info={"device_info": {"custom_user_access": descr}},
                    parent=self,
                )
                setattr(
                    self,
                    user_access_name,
                    self._custom_rpc_methods[user_access_name],
                )

    def update_config(self, update: dict) -> None:
        """
        Updates the device configuration.

        Args:
            update (dict): The update dictionary.

        """
        self.root.parent.config_helper.send_config_request(
            action="update", config={self.name: update}
        )


class DeviceBase(RPCBase, Device):
    """
    Device (bluesky interface):
    * trigger
    * read
    * describe
    * stage
    * unstage
    * pause
    * resume
    """

    @property
    def enabled(self):
        # pylint: disable=protected-access
        return self.root._config["enabled"]

    @enabled.setter
    def enabled(self, val):
        # pylint: disable=protected-access
        self.update_config({"enabled": val})
        self.root._config["enabled"] = val

    @rpc
    def trigger(self, rpc_id: str):
        """
        Triggers the device.
        """

    @rpc
    def stop(self):
        """
        Stops the device.
        """

    @rpc
    def read(self, cached=False, use_readback=True, filter_signal=True):
        if use_readback:
            val = self.parent.producer.get(MessageEndpoints.device_readback(self.name))
        else:
            val = self.parent.producer.get(MessageEndpoints.device_read(self.name))

        if not val:
            return None
        signals = messages.DeviceMessage.loads(val).content["signals"]
        if filter_signal and signals.get(self.name):
            return signals.get(self.name)
        return signals

    @rpc
    def read_configuration(self):
        """
        Reads the device configuration.
        """

    @rpc
    def describe(self):
        """
        Describes the device and yields information about the device's signals, including
        the signal's name, source, shape, data type, precision etc.
        """

    @rpc
    def stage(self):
        """
        Stages the device. This method should normally not be called directly, but rather
        via the scan server.
        """

    @rpc
    def unstage(self):
        """
        Unstages the device. This method should normally not be called directly, but rather
        via the scan server.
        """

    @rpc
    def summary(self):
        """
        Provides a summary of the device, all associated signals and their type.
        """


class Signal(DeviceBase):
    """
    Signal:
    * trigger
    * get
    * put
    * set
    * value
    * read
    * describe
    * limits
    * low limit
    * high limit
    """

    @rpc
    def get(self):
        """
        Gets the signal value.
        """

    @rpc
    def put(self, val):
        """
        Puts the signal value.
        """

    @rpc
    def set(self, val):
        """
        Sets the signal value.
        """

    @rpc
    def value(self):
        pass

    @rpc
    def limits(self):
        pass

    @rpc
    def low_limit(self):
        pass

    @rpc
    def high_limit(self):
        pass


class Positioner(DeviceBase):
    """
    Positioner:
    * trigger
    * read
    * set
    * stop
    * settle_time
    * timeout
    * egu
    * limits
    * low_limit
    * high_limit
    * move
    * position
    * moving
    """

    @rpc
    def set(self, val):
        pass

    @rpc
    def stop(self):
        pass

    @rpc
    def settle_time(self):
        pass

    @rpc
    def timeout(self):
        pass

    @rpc
    def egu(self):
        pass

    @property
    def limits(self):
        return self._config["deviceConfig"].get("limits", [0, 0])

    @limits.setter
    def limits(self, val: list):
        self.update_config({"deviceConfig": {"limits": val}})

    @property
    def low_limit(self):
        return self.limits[0]

    @low_limit.setter
    def low_limit(self, val: float):
        limits = [val, self.high_limit]
        self.update_config({"deviceConfig": {"limits": limits}})

    @property
    def high_limit(self):
        return self.limits[1]

    @high_limit.setter
    def high_limit(self, val: float):
        limits = [self.low_limit, val]
        self.update_config({"deviceConfig": {"limits": limits}})

    def move(self, val: float, relative=False):
        return self.parent.parent.scans.mv(self, val, relative=relative)

    @rpc
    def position(self):
        pass

    @rpc
    def moving(self):
        pass


class DMClient(DeviceManagerBase):
    def __init__(self, parent):
        super().__init__(parent.connector)
        self.parent = parent

    def _get_device_info(self, device_name) -> messages.DeviceInfoMessage:
        msg = messages.DeviceInfoMessage.loads(
            self.producer.get(MessageEndpoints.device_info(device_name))
        )
        return msg

    def _load_session(self, _device_cls=None, *_args):
        time.sleep(1)
        if self._is_config_valid():
            for dev in self._session["devices"]:
                try:
                    msg = self._get_device_info(dev.get("name"))
                    self._add_device(dev, msg)
                except Exception as exc:
                    content = traceback.format_exc()
                    logger.error(f"Failed to load device {dev}: {content}")

    def _add_device(self, dev: dict, msg: messages.DeviceInfoMessage):
        name = msg.content["device"]
        info = msg.content["info"]

        base_class = info["device_info"]["device_base_class"]

        if base_class == "device":
            logger.info(f"Adding new device {name}")
            obj = DeviceBase(name, info, parent=self)
        elif base_class == "positioner":
            logger.info(f"Adding new positioner {name}")
            obj = Positioner(name, info, parent=self)
        elif base_class == "signal":
            logger.info(f"Adding new signal {name}")
            obj = Signal(name, info, parent=self)
        else:
            logger.error(f"Trying to add new device {name} of type {base_class}")

        obj._config = dev
        self.devices._add_device(name, obj)
