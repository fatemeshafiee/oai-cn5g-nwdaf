import networkx as nx
import pandas as pd
import pytest

from src.functions import ip_to_int, extract_flow_info, compute_lcc, build_graph_per_batch


# ---------- ip_to_int ----------

def test_ip_to_int_ipv4_value_and_family():
    value, family = ip_to_int("192.168.1.1")
    assert value == 3232235777
    assert family == "IP4"


def test_ip_to_int_boundaries():
    assert ip_to_int("0.0.0.0")[0] == 0
    assert ip_to_int("255.255.255.255")[0] == 4294967295


def test_ip_to_int_ipv6_is_tagged_separately():
    value, family = ip_to_int("::1")
    assert family == "IP6"
    assert value == 1


# ---------- extract_flow_info ----------

def test_extract_flow_info_parses_all_fields():
    packet_filter = '{"SeId": 7, "SrcIp": "10.45.0.2", "DstIp": "8.8.8.8", "SrcPort": 5060, "DstPort": 443}'
    se_id, src_ip, dst_ip, src_port, dst_port = extract_flow_info(packet_filter)
    assert (se_id, src_ip, dst_ip, src_port, dst_port) == (7, "10.45.0.2", "8.8.8.8", 5060, 443)


def test_extract_flow_info_tolerates_embedded_newlines():
    """The UPF sends filters with line breaks, which the parser strips before decoding."""
    packet_filter = '{"SeId": 1,\n "SrcIp": "10.0.0.1",\n "DstIp": "10.0.0.2",\n "SrcPort": 80,\n "DstPort": 90}'
    assert extract_flow_info(packet_filter)[1] == "10.0.0.1"


def test_extract_flow_info_missing_keys_yield_none():
    se_id, src_ip, _, _, _ = extract_flow_info('{"SrcIp": "10.0.0.1"}')
    assert se_id is None
    assert src_ip == "10.0.0.1"


def test_extract_flow_info_rejects_malformed_json():
    with pytest.raises(ValueError):
        extract_flow_info("{not json")


# ---------- compute_lcc ----------

def test_compute_lcc_fully_connected_triangle_is_one():
    g = nx.DiGraph()
    for a, b in [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B"), ("A", "C"), ("C", "A")]:
        g.add_edge(a, b)
    assert compute_lcc(g) == {"A": 1.0, "B": 1.0, "C": 1.0}


def test_compute_lcc_path_middle_node_has_unconnected_neighbours():
    g = nx.DiGraph()
    for a, b in [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B")]:
        g.add_edge(a, b)
    lcc = compute_lcc(g)
    assert lcc["B"] == 0.0   # A and C are not connected to each other
    assert lcc["A"] == 0.0   # fewer than two neighbours


# ---------- build_graph_per_batch ----------

def test_build_graph_per_batch_creates_both_directions_with_weights():
    df = pd.DataFrame([{"src_ip": "10.0.0.1", "dst_ip": "10.0.0.2", "src_pkts": 12, "dst_pkts": 5}])
    g = build_graph_per_batch(df)
    assert g.has_edge("10.0.0.1", "10.0.0.2")
    assert g.has_edge("10.0.0.2", "10.0.0.1")
    assert g["10.0.0.1"]["10.0.0.2"]["weight"] == 12
    assert g["10.0.0.2"]["10.0.0.1"]["weight"] == 5
