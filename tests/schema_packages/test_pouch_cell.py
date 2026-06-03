import os
import pytest

from nomad.client import normalize_all, parse


@pytest.mark.skip(reason="Deprecated: requires update to new data model")
def test_pouch_cell_battery():
    """Test PouchCellBattery schema with required dimensions."""
    path = os.path.join("tests", "data", "pouch_cell.archive.yaml")

    archive = parse(path)[0]
    normalize_all(archive)

    data = archive.data

    # Check entry type
    assert data.m_def.name == "PouchCellBattery"

    # Basic metadata
    assert data.lab_id == "PC_001"
    assert data.name == "pouch_cell_01"

    # Required cathode dimensions
    assert data.cathode_length.magnitude == 50.5
    assert data.cathode_width.magnitude == 40.0
    
    # Number of layers
    assert data.number_of_layers == 3

    # Optional pouch dimensions
    assert data.pouch_length.magnitude == 60.0
    assert data.pouch_width.magnitude == 50.0
    assert data.pouch_height.magnitude == 5.5

    # Check components
    assert data.components is not None
    assert hasattr(data.components, "anode_q")
    assert hasattr(data.components, "cathode_q")
    assert hasattr(data.components, "electrolyte_q")
    assert hasattr(data.components, "separator_q")

    # Check sample identifiers
    assert data.sample_identifiers.sample_id == "PC_DEF456"
