import os
import pytest

from nomad.client import normalize_all, parse


@pytest.mark.skip(reason="Deprecated: requires update to new data model")
def test_schema_package():
    base = os.path.join('tests', 'data')

    files = [
        'anode.archive.yaml',
        'cathode.archive.yaml',
        'electrolyte.archive.yaml',
        'separator.archive.yaml',
        'battery_sample.archive.yaml',
    ]

    # Load archives
    archives = [parse(os.path.join(base, f))[0] for f in files]

    # Normalize each archive independently
    for a in archives:
        normalize_all(a)

    # Find BatterySample
    battery = next(a for a in archives if a.data.m_def.name == "BatterySample")
    data = battery.data

    # Basic metadata
    assert data.name == "bat_01"

    comp = data.components

    # Extract reference pointers (string or MProxy)
    def ref_value(r):
        if hasattr(r, "m_proxy_value"):
            return r.m_proxy_value
        return r

    # Expected references (note the "/")
    assert ref_value(comp.anode_q) == "#/anode_01"
    assert ref_value(comp.cathode_q) == "#/cathode_01"
    assert ref_value(comp.electrolyte_q) == "#/electrolyte_01"
    assert ref_value(comp.separator_q) == "#/separator_01"

    # Additional checks
    assert data.sample_identifiers.sample_id == "ABC123"
