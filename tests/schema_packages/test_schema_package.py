import os

from nomad.client import normalize_all, parse
from nomad.datamodel.context import ServerContext


def test_schema_package():
    base = os.path.join('tests', 'data')

    files = [
        'anode.archive.yaml',
        'cathode.archive.yaml',
        'electrolyte.archive.yaml',
        'separator.archive.yaml',
        'battery_sample.archive.yaml',
    ]

    # Load entries
    archives = [parse(os.path.join(base, f))[0] for f in files]

    # Normalize each independently
    for a in archives:
        normalize_all(a)

    # Build a map of entry names → archives
    # NOMAD 1.x resolves '#name' via context._archive_dict
    archive_dict = {a.data.name: a for a in archives}

    # Assign context manually
    for a in archives:
        a.m_context._archive_dict = archive_dict

    # Get battery archive
    battery = next(a for a in archives if a.data.m_def.name == "BatterySample")

    ctx = battery.m_context

    # Resolve via get_reference()
    anode = ctx.get_reference(battery.data.components.anode_q)
    cathode = ctx.get_reference(battery.data.components.cathode_q)
    electrolyte = ctx.get_reference(battery.data.components.electrolyte_q)
    separator = ctx.get_reference(battery.data.components.separator_q)

    # Assertions
    assert battery.data.name == "bat_01"
    assert anode.mass.magnitude == 1.2
    assert cathode.mass_active_material.magnitude == 2.1
    assert electrolyte.volume.magnitude == 1.1
    assert separator.thickness.magnitude == 20.0
    assert battery.data.sample_identifiers.sample_id == "ABC123"