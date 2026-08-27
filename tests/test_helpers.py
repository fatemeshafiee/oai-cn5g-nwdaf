import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent
                     / "components" / "nwdaf-engine-bot-detection" / "src"))

from functions import ip_to_int


def test_ip_to_int_boundaries():
    assert ip_to_int("0.0.0.0") == 0
    assert ip_to_int("255.255.255.255") == 4294967295


def test_ip_to_int_known_value():
    assert ip_to_int("192.168.1.1") == 3232235777
