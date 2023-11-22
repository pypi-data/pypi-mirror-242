import logging

import pytest

from pyliblorawan.models import Uplink
from pyliblorawan.network_servers.helpers import normalize_unknown_uplink
from pyliblorawan.network_servers.ttn import TTN


def test_ttn_uplink(caplog_debug: pytest.LogCaptureFixture, ttn_uplink: Uplink):
    uplink = normalize_unknown_uplink(ttn_uplink)

    assert uplink.device_eui == "FEEDABCD00000002"
    assert uplink.f_port == 123
    assert uplink.payload == bytes.fromhex("FE00ED")

    assert caplog_debug.record_tuples == []


def test_unknown_ns(caplog_debug: pytest.LogCaptureFixture):
    with pytest.raises(ValueError) as e:
        normalize_unknown_uplink({"TEST": "UPLINK"})

    assert str(e.value) == "Unable to parse uplink, unknown NS"
    assert caplog_debug.record_tuples == [
        (
            "pyliblorawan.network_servers.helpers",
            logging.ERROR,
            "Unable to parse uplink, unknown NS",
        ),
        ("pyliblorawan.network_servers.helpers", logging.ERROR, "{'TEST': 'UPLINK'}"),
    ]
