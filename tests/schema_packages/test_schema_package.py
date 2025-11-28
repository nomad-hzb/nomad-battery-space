import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    archives = parse(os.path.join('tests', 'data', 'test.archive.yaml'))
    
    entry_archive = archives[4] # BatterySample is the 5th entry
    normalize_all(entry_archive)

    assert entry_archive.data.name == "bat_01"

    # ---- resolve references ----
    ctx = entry_archive.m_context

    anode = ctx.resolve(entry_archive.data.components.anode_q)
    cathode = ctx.resolve(entry_archive.data.components.cathode_q)
    electrolyte = ctx.resolve(entry_archive.data.components.electrolyte_q)
    separator = ctx.resolve(entry_archive.data.components.separator_q)

    # ---- assertions ----
    assert anode.mass.magnitude == 1.2
    assert cathode.mass_active_material.magnitude == 2.1
    assert electrolyte.volume.magnitude == 1.1
    assert separator.thickness.magnitude == 20.0

    assert entry_archive.data.sample_identifiers.sample_id == "ABC123"
