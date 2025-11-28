import os

from nomad.client import normalize_all, parse


def test_electrolyte_component():
    path = os.path.join("tests", "data", "electrolyte.archive.yaml")

    archive = parse(path)[0]
    normalize_all(archive)

    data = archive.data

    assert data.m_def.name == "Electrolyte"

    # Values from test YAML
    assert data.name == "electrolyte_01"
    assert data.mass.magnitude == 0.9
    assert data.volume.magnitude == 1.1
    assert data.state == "Liquid" 