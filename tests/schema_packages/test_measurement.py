import os

import pytest
from nomad.client import normalize_all, parse

from nomad_battery_space.schema_packages.hzb_bs_measurement_package import (
    BS_Measurement,
    BS_SampleReference,
)


def load(file_name):
    archive = parse(os.path.join('tests', 'data', file_name))[0]
    normalize_all(archive)
    return archive


def test_measurement_with_files():
    data = load('measurement.archive.yaml').data

    assert isinstance(data, BS_Measurement)
    assert data.data_file == ['cell_01_cycling.dta', 'cell_01_operando.nxs']
    assert data.method == 'galvanostatic cycling'


@pytest.mark.parametrize(
    'file_name',
    [
        'electrode_material.archive.yaml',
        'electrolyte_stock.archive.yaml',
        'separator_stock.archive.yaml',
        'coin_cell.archive.yaml',
    ],
)
def test_battery_samples_can_be_referenced(file_name):
    """All battery samples (ELNSubstance, not CompositeSystem) are accepted."""
    sample = load(file_name).data
    measurement = BS_Measurement(
        name='test', samples=[BS_SampleReference(reference=sample)]
    )

    assert measurement.samples[0].reference is sample
