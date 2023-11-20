"""Contains device classes."""
from __future__ import annotations

from abc import ABC
import asyncio
from functools import cache
from typing import ClassVar, Iterable

from pyplumio.const import ATTR_FRAME_ERRORS, ATTR_LOADED, DeviceType, FrameType
from pyplumio.exceptions import ParameterNotFoundError, UnknownDeviceError
from pyplumio.frames import DataFrameDescription, Frame, Request, get_frame_handler
from pyplumio.helpers.event_manager import EventManager
from pyplumio.helpers.factory import factory
from pyplumio.helpers.parameter import SET_RETRIES, Parameter
from pyplumio.helpers.typing import ParameterValueType
from pyplumio.structures.network_info import NetworkInfo
from pyplumio.utils import to_camelcase


@cache
def get_device_handler(device_type: int) -> str:
    """Return module name and class name for a given device type."""
    try:
        device_type = DeviceType(device_type)
    except ValueError as e:
        raise UnknownDeviceError(f"Unknown device ({device_type})") from e

    type_name = to_camelcase(
        device_type.name, overrides={"ecomax": "EcoMAX", "ecoster": "EcoSTER"}
    )
    return f"devices.{type_name.lower()}.{type_name}"


@cache
def get_device_handler_and_name(device_type: int) -> tuple[str, str]:
    """Get device handler full path and lowercased class name."""
    handler = get_device_handler(device_type)
    class_name = handler.rsplit(".", 1)[1]
    return handler, class_name.lower()


class Device(ABC, EventManager):
    """Represents a device."""

    __slots__ = ("queue",)

    queue: asyncio.Queue

    def __init__(self, queue: asyncio.Queue):
        """Initialize a new device."""
        super().__init__()
        self.queue = queue

    async def set(
        self,
        name: str,
        value: ParameterValueType,
        timeout: float | None = None,
        retries: int = SET_RETRIES,
    ) -> bool:
        """Set a parameter value.

        Name should point to a valid parameter object, otherwise
        raise ParameterNotFoundError.
        """
        parameter = await self.get(name, timeout=timeout)
        if not isinstance(parameter, Parameter):
            raise ParameterNotFoundError(f"Parameter not found ({name})")

        return await parameter.set(value, retries=retries)

    def set_nowait(
        self,
        name: str,
        value: ParameterValueType,
        timeout: float | None = None,
        retries: int = SET_RETRIES,
    ) -> None:
        """Set a parameter value without waiting for the result."""
        self.create_task(self.set(name, value, timeout, retries))


class Addressable(Device, ABC):
    """Represents an addressable device."""

    __slots__ = ("address", "_network", "_setup_frames")

    address: ClassVar[int]
    _network: NetworkInfo
    _setup_frames: Iterable[DataFrameDescription]

    def __init__(self, queue: asyncio.Queue, network: NetworkInfo):
        """Initialize a new addressable device."""
        super().__init__(queue)
        self._network = network

    def __int__(self) -> int:
        """Return the device address."""
        return int(self.address)

    def handle_frame(self, frame: Frame) -> None:
        """Handle a frame received from the addressable device."""
        frame.sender = self
        if frame.data is not None:
            for name, value in frame.data.items():
                self.dispatch_nowait(name, value)

    async def async_setup(self) -> bool:
        """Setup an addressable device."""
        results = await asyncio.gather(
            *{
                self.create_task(
                    self.request(description.provides, description.frame_type)
                )
                for description in self._setup_frames
            },
            return_exceptions=True,
        )

        errors = [
            result.args[1] for result in results if isinstance(result, ValueError)
        ]

        await self.dispatch(ATTR_FRAME_ERRORS, errors)
        await self.dispatch(ATTR_LOADED, True)
        return True

    async def request(
        self,
        name: str,
        frame_type: FrameType,
        retries: int = 3,
        timeout: float = 3.0,
    ):
        """Send request for a data and wait for a value to become
        available.

        If value is not available before timeout, retry request.
        """
        request: Request = factory(
            get_frame_handler(frame_type), recipient=self.address
        )
        while retries > 0:
            try:
                self.queue.put_nowait(request)
                return await self.get(name, timeout=timeout)
            except asyncio.TimeoutError:
                retries -= 1

        raise ValueError(f'could not request "{name}"', frame_type)


class SubDevice(Device, ABC):
    """Represents the sub-device."""

    __slots__ = ("parent", "index")

    parent: Addressable
    index: int

    def __init__(self, queue: asyncio.Queue, parent: Addressable, index: int = 0):
        """Initialize a new sub-device object."""
        super().__init__(queue)
        self.parent = parent
        self.index = index
