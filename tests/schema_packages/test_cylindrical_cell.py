import os

import pytest
from nomad.client import normalize_all, parse


@pytest.mark.skip(reason="Deprecated: requires update to new data model")
def test_cylindrical_cell_battery():
    """Test CylindricalCellBattery schema with specifications."""
    path = os.path.join("tests", "data", "cylindrical_cell.archive.yaml")

    archive = parse(path)[0]
    normalize_all(archive)

    data = archive.data

    # Check entry type
    assert data.m_def.name == "CylindricalCellBattery"

    # Basic metadata
    assert data.lab_id == "CYL_001"
    assert data.name == "cylindrical_cell_01"

    # Case identification
    assert data.case_id == "18650"

    # Cathode dimensions
    assert data.cathode_length.magnitude == 45.0
    assert data.cathode_width.magnitude == 42.0

    # Cylindrical dimensions
    assert data.cylindrical_length.magnitude == 65.0
    assert data.cylindrical_diameter.magnitude == 18.3

    # Check components
    assert data.components is not None
    assert hasattr(data.components, "anode_q")
    assert hasattr(data.components, "cathode_q")
    assert hasattr(data.components, "electrolyte_q")
    assert hasattr(data.components, "separator_q")

    # Check sample identifiers
    assert data.sample_identifiers.sample_id == "CYL_GHI789"
