import os

from nomad.client import normalize_all, parse


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

    # Identify the battery sample record
    battery = next(a for a in archives if a.data.m_def.name == "BatterySample")

    # Normalize so references resolve
    normalize_all(battery)

    ctx = battery.m_context

    # Resolve linked entries
    anode = ctx.resolve(battery.data.components.anode_q)
    cathode = ctx.resolve(battery.data.components.cathode_q)
    electrolyte = ctx.resolve(battery.data.components.electrolyte_q)
    separator = ctx.resolve(battery.data.components.separator_q)

    # Assertions
    assert battery.data.name == "bat_01"
    assert anode.mass.magnitude == 1.2
    assert cathode.mass_active_material.magnitude == 2.1
    assert electrolyte.volume.magnitude == 1.1
    assert separator.thickness.magnitude == 20.0
    assert battery.data.sample_identifiers.sample_id == "ABC123"
