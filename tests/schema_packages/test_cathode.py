import os

from nomad.client import normalize_all, parse


def test_cathode_component():
    path = os.path.join("tests", "data", "cathode.archive.yaml")

    archive = parse(path)[0]
    normalize_all(archive)

    data = archive.data

    assert data.m_def.name == "Cathode"

    # Values from test YAML
    assert data.name == "cathode_01"
    assert data.mass.magnitude == 3.4
    assert data.mass_active_material.magnitude == 2.1
