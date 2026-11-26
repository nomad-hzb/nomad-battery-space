import pytest
from nomad.client import normalize_all
from nomad.datamodel import EntryArchive, EntryMetadata

from nomad_battery_space.schema_packages.hzb_bs_assembly_package import (
    CoinCellBattery,
)
from nomad_battery_space.schema_packages.hzb_bs_measurement_package import (
    BS_Measurement,
)
from nomad_battery_space.schema_packages.hzb_bs_package import (
    BatterySample,
    BS_Chemical,
    ElectrodeMaterial,
    ElectrodeSample,
    ElectrodeSheet,
    ElectrolyteSample,
    ElectrolyteStock,
    SeparatorSample,
    SeparatorStock,
)

ENTRY_CLASSES = [
    BS_Chemical,
    ElectrodeMaterial,
    ElectrodeSheet,
    ElectrolyteStock,
    SeparatorStock,
    ElectrodeSample,
    ElectrolyteSample,
    SeparatorSample,
    BatterySample,
    CoinCellBattery,
    BS_Measurement,
]

MAINFILE = 'my_new_sample.archive.json'


def _normalize(data):
    archive = EntryArchive(metadata=EntryMetadata(mainfile=MAINFILE), data=data)
    normalize_all(archive)
    return archive


@pytest.mark.parametrize('cls', ENTRY_CLASSES, ids=lambda c: c.__name__)
def test_entry_name_without_name_in_raw_file(cls):
    """Right after "create entry" the raw file has no name: the entry name must be
    the derived name, not the file name."""
    archive = _normalize(cls())
    assert archive.data.name == 'my new sample'
    assert archive.metadata.entry_name == 'my new sample'


@pytest.mark.parametrize('cls', ENTRY_CLASSES, ids=lambda c: c.__name__)
def test_entry_name_with_name_in_raw_file(cls):
    archive = _normalize(cls(name='LP30 batch 3'))
    assert archive.data.name == 'LP30 batch 3'
    assert archive.metadata.entry_name == 'LP30 batch 3'
