import os

import pytest
from nomad.client import normalize_all, parse


@pytest.mark.skip(reason="Deprecated: requires update to new data model")
def test_separator_component():
    path = os.path.join("tests", "data", "separator.archive.yaml")

    archive = parse(path)[0]
    normalize_all(archive)

    data = archive.data

    assert data.m_def.name == "Separator"

    # Values from test YAML
    assert data.name == "separator_01"
    assert data.thickness.magnitude == 20.0
