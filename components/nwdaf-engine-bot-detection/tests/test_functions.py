from src.functions import ip_to_int


def test_ip_to_int_ipv4():
    value, family = ip_to_int("192.168.1.1")
    assert value == 3232235777
    assert family == "IP4"


def test_ip_to_int_boundaries():
    assert ip_to_int("0.0.0.0")[0] == 0
    assert ip_to_int("255.255.255.255")[0] == 4294967295


def test_ip_to_int_ipv6_is_tagged():
    _, family = ip_to_int("::1")
    assert family == "IP6"
