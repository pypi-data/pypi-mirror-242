import datetime

import pytest

from pyliblorawan.models import Device, DeviceParser, NetworkServer, Sensors, Uplink


def test_device():
    device = Device("aa11223344556677", "test-name")
    assert device.device_eui == "AA11223344556677"
    assert device.name == "test-name"
    with pytest.raises(AttributeError):
        device.device_eui = "exception"  # type: ignore[misc]
    with pytest.raises(AttributeError):
        device.name = "exception"  # type: ignore[misc]
    assert device.device_eui == "AA11223344556677"
    assert device.name == "test-name"
    assert device == Device("aa11223344556677", "test-name")


def test_sensors_battery():
    sensors = Sensors()

    sensors.battery = 0.0
    assert sensors.battery == 0
    assert isinstance(sensors.battery, float)
    sensors.battery = 100
    assert sensors.battery == 100.0

    with pytest.raises(ValueError) as e:
        sensors.battery = -0.01
    assert str(e.value) == 'Battery value must be in [0:100], not "-0.01"'
    with pytest.raises(ValueError) as e:
        sensors.battery = 100.01
    assert str(e.value) == 'Battery value must be in [0:100], not "100.01"'
    assert sensors.battery == 100.0


def test_sensors_battery_level():
    sensors = Sensors()

    sensors.battery_level = 0.0
    assert sensors.battery_level == 0
    assert isinstance(sensors.battery_level, float)
    sensors.battery_level = 3.4
    assert sensors.battery_level == 3.4

    with pytest.raises(ValueError) as e:
        sensors.battery_level = -0.01
    assert str(e.value) == 'Battery level value must be positive, not "-0.01"'
    assert sensors.battery_level == 3.4


def test_sensors_humidity():
    sensors = Sensors()

    sensors.humidity = 0.0
    assert sensors.humidity == 0.0
    sensors.humidity = 12.345
    assert sensors.humidity == 12.345

    with pytest.raises(ValueError) as e:
        sensors.humidity = -0.01
    assert str(e.value) == 'Humidity must be in range [0; 100], not "-0.01"'
    with pytest.raises(ValueError) as e:
        sensors.humidity = 100.01
    assert str(e.value) == 'Humidity must be in range [0; 100], not "100.01"'
    assert sensors.humidity == 12.345


def test_sensors_illuminance():
    sensors = Sensors()

    sensors.illuminance = 0
    assert sensors.illuminance == 0
    sensors.illuminance = 12345
    assert sensors.illuminance == 12345

    with pytest.raises(ValueError) as e:
        sensors.illuminance = -0.01
    assert str(e.value) == 'Illuminance must be positive, not "-0.01"'
    assert sensors.illuminance == 12345


def test_sensors_pir_status():
    sensors = Sensors()

    sensors.pir_status = True
    assert sensors.pir_status == True
    sensors.pir_status = False
    assert sensors.pir_status == False


def test_sensors_temperature():
    sensors = Sensors()

    sensors.temperature = -12.34
    assert sensors.temperature == -12.34
    sensors.temperature = 43.21
    assert sensors.temperature == 43.21


def test_sensors_time_since_last_event():
    sensors = Sensors()

    sensors.time_since_last_event = 10
    assert sensors.time_since_last_event == 10
    sensors.time_since_last_event = 0
    assert sensors.time_since_last_event == 0
    sensors.time_since_last_event = datetime.timedelta(days=1)  # type: ignore[assignment]
    assert isinstance(sensors.time_since_last_event, int)
    assert sensors.time_since_last_event == 86400

    with pytest.raises(ValueError) as e:
        sensors.time_since_last_event = -1
    assert str(e.value) == 'Time since last event value must be positive, not "-1"'
    assert sensors.time_since_last_event == 86400


def test_sensors_total_event_counter():
    sensors = Sensors()

    sensors.total_event_counter = 10
    assert sensors.total_event_counter == 10
    sensors.total_event_counter = 0
    assert sensors.total_event_counter == 0

    with pytest.raises(ValueError) as e:
        sensors.total_event_counter = -1
    assert str(e.value) == 'Total event counter value must be positive, not "-1"'
    assert sensors.total_event_counter == 0


def test_uplink():
    payload = bytes.fromhex("0099")
    uplink = Uplink("FEEDABCD00000002", payload, 5)

    assert uplink.device_eui == "FEEDABCD00000002"
    assert uplink.payload == bytes.fromhex("0099")
    assert uplink.f_port == 5
    assert isinstance(uplink.sensors, Sensors)

    with pytest.raises(AttributeError):
        uplink.payload = bytes.fromhex("11")  # type: ignore[misc]
    with pytest.raises(AttributeError):
        uplink.f_port = 3  # type: ignore[misc]


@pytest.mark.asyncio
async def test_device_parser():
    payload = bytes.fromhex("0099")
    uplink = Uplink("FEEDABCD00000002", payload, 5)

    with pytest.raises(NotImplementedError) as e:
        await DeviceParser().parse_uplink(uplink)
    assert str(e.value) == "To be implemented in the specific device object"


@pytest.mark.asyncio
async def test_network_server():
    with pytest.raises(NotImplementedError):
        NetworkServer().is_compatible_uplink({})

    with pytest.raises(NotImplementedError):
        NetworkServer().normalize_uplink({})

    with pytest.raises(NotImplementedError):
        ns = NetworkServer()
        await ns.list_device_euis(None)  # type: ignore[arg-type]
