"""Defines models used by the library."""
import datetime

import aiohttp


class Device:
    """Holds a LoRaWAN device representation."""

    def __init__(self, device_eui: str, name: str) -> None:
        """Construct the Device object.

        :param device_eui: LoRaWAN IEEE-64 Extended Unique Identifier, as hex string
        :param name: Device name
        """
        self._device_eui = device_eui.upper()
        self._name = name

    @property
    def device_eui(self) -> str:
        """LoRaWAN IEEE-64 Extended Unique Identifier, as hex string."""
        return self._device_eui

    @property
    def name(self) -> str:
        """Device name."""
        return self._name

    def __eq__(self, __value: object) -> bool:
        return self.__dict__ == __value.__dict__


class Sensors:
    """Holds parsed sensor values."""

    @property
    def battery(self) -> float:
        """Remaining battery, in %."""
        return self._battery

    @battery.setter
    def battery(self, value: int | float) -> None:
        value = float(value)
        if value < 0.0 or value > 100.0:
            raise ValueError(f'Battery value must be in [0:100], not "{value}"')
        self._battery = value

    @property
    def battery_level(self) -> float:
        """Battery level, in Volts."""
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value: int | float) -> None:
        value = float(value)
        if value < 0.0:
            raise ValueError(f'Battery level value must be positive, not "{value}"')
        self._battery_level = value

    @property
    def humidity(self) -> float:
        """Relative humidity, in %."""
        return self._humidity

    @humidity.setter
    def humidity(self, value: int) -> None:
        if value < 0.0 or value > 100.0:
            raise ValueError(f'Humidity must be in range [0; 100], not "{value}"')
        self._humidity = value

    @property
    def illuminance(self) -> int:
        """illuminance, in Lux."""
        return self._illuminance

    @illuminance.setter
    def illuminance(self, value: int) -> None:
        if value < 0:
            raise ValueError(f'Illuminance must be positive, not "{value}"')
        self._illuminance = value

    @property
    def pir_status(self) -> bool:
        """Infrared presence detection."""
        return self._pir_status

    @pir_status.setter
    def pir_status(self, value: bool) -> None:
        self._pir_status = value

    @property
    def temperature(self) -> float:
        """Temperature in °C."""
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        self._temperature = value

    @property
    def time_since_last_event(self) -> int:
        """Elapsed time since last event.

        :return: Time in seconds
        """
        return self._time_since_last_event

    @time_since_last_event.setter
    def time_since_last_event(self, value: datetime.timedelta | int) -> None:
        """Elapsed time since last event.

        :param value: Time in seconds or datetime.timedelta()
        """
        if isinstance(value, datetime.timedelta):
            value = int(value.total_seconds())
        if value < 0:
            raise ValueError(
                f'Time since last event value must be positive, not "{value}"'
            )
        self._time_since_last_event = value

    @property
    def total_event_counter(self) -> int:
        """Number of events that occurred in the past."""
        return self._total_event_counter

    @total_event_counter.setter
    def total_event_counter(self, value: int) -> None:
        if value < 0:
            raise ValueError(
                f'Total event counter value must be positive, not "{value}"'
            )
        self._total_event_counter = value


class Uplink:
    """Generic uplink class to hold parsed data."""

    def __init__(self, device_eui: str, payload: bytes, f_port: int) -> None:
        """Construct the Uplink object.

        :param payload: Uplink payload in bytes
        :param f_port: LoRaWAN frame port
        """
        self._device_eui = device_eui.upper()
        self._payload = payload
        self._f_port = f_port

        self.sensors = Sensors()

    @property
    def device_eui(self) -> str:
        """LoRaWAN device EUI."""
        return self._device_eui

    @property
    def payload(self) -> bytes:
        """Uplink payload in bytes."""
        return self._payload

    @property
    def f_port(self) -> int:
        """LoRaWAN FPort bytes."""
        return self._f_port


class DeviceParser:
    """Interface for device uplink/downlink parser"""

    @staticmethod
    async def parse_uplink(uplink: Uplink) -> Uplink:
        """Parse binary payload depending on FPort"""
        raise NotImplementedError("To be implemented in the specific device object")


class NetworkServer:
    @staticmethod
    def is_compatible_uplink(uplink: dict) -> bool:
        """Return True if the payload is compatible with this NS"""
        raise NotImplementedError()

    async def list_device_euis(self, session: aiohttp.ClientSession) -> list[Device]:
        """List device euis of accessible device on theNS, can be limited to an application"""
        raise NotImplementedError()

    @staticmethod
    def normalize_uplink(uplink: dict) -> Uplink:
        """Parse an uplink json to internal object model when NS is known"""
        raise NotImplementedError()
