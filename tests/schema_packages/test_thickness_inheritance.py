import pytest
from nomad.client import normalize_all
from nomad.datamodel import EntryArchive, EntryMetadata

from nomad_battery_space.schema_packages.hzb_bs_package import (
    ElectrodeSample,
    ElectrodeSheet,
    SeparatorSample,
    SeparatorStock,
)
from nomad_battery_space.schema_packages.utilities import DimensionsAndWeights

# (sample class, parent class, name of the reference to the parent)
CASES = [
    (ElectrodeSample, ElectrodeSheet, 'electrode_sheet'),
    (SeparatorSample, SeparatorStock, 'separator_stock'),
]
IDS = [case[0].__name__ for case in CASES]


def make_sample(sample_cls, parent_cls, ref_name, parent_thickness, own_thickness):
    parent = parent_cls(
        name='parent',
        dimensions_and_weights=DimensionsAndWeights(thickness=parent_thickness),
    )
    sample = sample_cls(name='sample', **{ref_name: parent})
    if own_thickness is not None:
        sample.dimensions_and_weights = DimensionsAndWeights(thickness=own_thickness)
    archive = EntryArchive(data=sample, metadata=EntryMetadata())
    normalize_all(archive)
    return sample


@pytest.mark.parametrize('sample_cls, parent_cls, ref_name', CASES, ids=IDS)
def test_thickness_taken_from_parent_if_empty(sample_cls, parent_cls, ref_name):
    sample = make_sample(sample_cls, parent_cls, ref_name, 25.0, None)

    assert sample.dimensions_and_weights.thickness.magnitude == 25.0


@pytest.mark.parametrize('sample_cls, parent_cls, ref_name', CASES, ids=IDS)
def test_own_thickness_is_kept(sample_cls, parent_cls, ref_name):
    sample = make_sample(sample_cls, parent_cls, ref_name, 25.0, 20.0)

    assert sample.dimensions_and_weights.thickness.magnitude == 20.0


@pytest.mark.parametrize('sample_cls, parent_cls, ref_name', CASES, ids=IDS)
def test_no_parent_thickness(sample_cls, parent_cls, ref_name):
    sample = make_sample(sample_cls, parent_cls, ref_name, None, None)

    assert (
        sample.dimensions_and_weights is None
        or sample.dimensions_and_weights.thickness is None
    )
