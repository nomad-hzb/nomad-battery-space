import os
import pytest

from nomad.client import normalize_all, parse


@pytest.mark.skip(reason="Deprecated: requires update to new data model")
def test_coin_cell_battery():
    """Test CoinCellBattery schema with manual case crimping."""
    path = os.path.join("tests", "data", "coin_cell.archive.yaml")

    archive = parse(path)[0]
    normalize_all(archive)

    data = archive.data

    # Check entry type
    assert data.m_def.name == "CoinCellBattery"

    # Basic metadata
    assert data.lab_id == "CC_001"
    assert data.name == "coin_cell_01"
    assert data.case_id == "CR2032"
    assert data.case_crimp == "manual"
    
    # Verify normalization: manual crimp should set pressure to None
    assert data.pressure is None

    # Check components
    assert data.components is not None
    assert hasattr(data.components, "anode_q")
    assert hasattr(data.components, "cathode_q")
    assert hasattr(data.components, "electrolyte_q")
    assert hasattr(data.components, "separator_q")

    # Check sample identifiers
    assert data.sample_identifiers.sample_id == "CC_ABC123"
