import os

import pytest
from nomad.client import normalize_all, parse
from nomad.datamodel import EntryArchive, EntryMetadata

from nomad_battery_space.schema_packages.hzb_bs_assembly_package import (
    CoinCellBattery,
)


def test_coin_cell_battery():
    """Manual crimping clears the pressure."""
    path = os.path.join('tests', 'data', 'coin_cell.archive.yaml')

    archive = parse(path)[0]
    normalize_all(archive)

    data = archive.data

    assert isinstance(data, CoinCellBattery)
    assert data.lab_id == 'CC_001'
    assert data.name == 'coin_cell_01'
    assert data.case_id == '2032'
    assert data.case_crimp == 'manual'
    assert data.pressure is None


def test_automatic_crimping_keeps_pressure():
    cell = CoinCellBattery(
        lab_id='CC_002', name='coin_cell_02', case_crimp='automatic', pressure=0.8
    )
    normalize_all(EntryArchive(data=cell, metadata=EntryMetadata()))

    assert cell.pressure.magnitude == 0.8


def test_battery_id_is_required():
    cell = CoinCellBattery(name='coin_cell_03')

    with pytest.raises(ValueError, match='battery ID'):
        cell.normalize(EntryArchive(data=cell, metadata=EntryMetadata()), None)
