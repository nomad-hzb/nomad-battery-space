import os

import pytest
from nomad.client import normalize_all, parse


@pytest.mark.skip(reason="Deprecated: requires update to new data model")
def test_anode_component():
    path = os.path.join("tests", "data", "anode.archive.yaml")

    archive = parse(path)[0]
    normalize_all(archive)

    data = archive.data

    # Basic properties
    assert data.m_def.name == "Anode"
    
    assert hasattr(data, "mass")
    assert hasattr(data, "area")

    # Values from test YAML
    assert data.name == "anode_01"
    assert data.mass.magnitude == 1.2
    assert data.area.magnitude == 0.95
