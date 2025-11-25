import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.name == "bat_01"
    assert entry_archive.data.components.anode.mass.magnitude == 1.2
    assert entry_archive.data.components.cathode.mass_active_material.magnitude == 2.1
    assert entry_archive.data.sample_identifiers.sample_id == "ABC123"
