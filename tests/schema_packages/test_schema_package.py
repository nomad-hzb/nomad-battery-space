import os

from nomad.client import normalize_all, parse


def test_schema_package():
    base = os.path.join('tests', 'data')
    battery_path = os.path.join(base, 'battery_sample.archive.yaml')

    # Load only the BatterySample archive
    entry_archive = parse(battery_path)[0]
    normalize_all(entry_archive)

    battery = entry_archive.data

    assert battery.name == "bat_01"

    # Check that the reference fields are set as expected
    # Depending on NOMAD version, .anode_q may be a string or a MProxy.
    anode_ref = battery.components.anode_q
    cathode_ref = battery.components.cathode_q
    electrolyte_ref = battery.components.electrolyte_q
    separator_ref = battery.components.separator_q

    # For MProxy, the raw reference is in .m_proxy_value
    if hasattr(anode_ref, "m_proxy_value"):
        anode_ref = anode_ref.m_proxy_value
        cathode_ref = cathode_ref.m_proxy_value
        electrolyte_ref = electrolyte_ref.m_proxy_value
        separator_ref = separator_ref.m_proxy_value

    assert anode_ref == "#anode_01"
    assert cathode_ref == "#cathode_01"
    assert electrolyte_ref == "#electrolyte_01"
    assert separator_ref == "#separator_01"

    assert battery.sample_identifiers.sample_id == "ABC123"