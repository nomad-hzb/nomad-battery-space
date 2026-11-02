import os

import pytest
from nomad.client import normalize_all, parse
from nomad.datamodel import EntryArchive, EntryMetadata
from nomad.datamodel.metainfo.basesections.v1 import ProcessStep

from nomad_battery_space.schema_packages.hzb_bs_package import (
    ElectrodeMaterial,
    ElectrodeMaterialReference,
    ElectrolyteStock,
    ElectrolyteStockReference,
    SeparatorStock,
    SeparatorStockReference,
)
from nomad_battery_space.schema_packages.utilities.processing import (
    SampleProcessing,
)

# (class, reference class, test data file, precursor name, precursor elements)
CASES = [
    (
        ElectrodeMaterial,
        ElectrodeMaterialReference,
        'electrode_material.archive.yaml',
        'NMC111_200um',
        ['Co', 'Li', 'Mn', 'Ni', 'O'],
    ),
    (
        ElectrolyteStock,
        ElectrolyteStockReference,
        'electrolyte_stock.archive.yaml',
        'LP30',
        ['C', 'F', 'H', 'Li', 'O', 'P'],
    ),
    (
        SeparatorStock,
        SeparatorStockReference,
        'separator_stock.archive.yaml',
        'Celgard_2400',
        ['C', 'H'],
    ),
]
IDS = [case[0].__name__ for case in CASES]


def load_precursor(file_name):
    archive = parse(os.path.join('tests', 'data', file_name))[0]
    normalize_all(archive)
    return archive


@pytest.mark.parametrize('cls, ref_cls, file_name, name, elements', CASES, ids=IDS)
def test_existing_entry_without_processing(cls, ref_cls, file_name, name, elements):
    """Entries without the new fields must load and normalize as before."""
    data = load_precursor(file_name).data

    assert isinstance(data, cls)
    assert data.name == name
    assert not data.precursors
    assert data.processing is None
    assert data.aggregated_elements == elements


@pytest.mark.parametrize('cls, ref_cls, file_name, name, elements', CASES, ids=IDS)
def test_precursors_only_accept_same_type(cls, ref_cls, file_name, name, elements):
    precursors = cls.m_def.all_sub_sections['precursors']
    assert precursors.sub_section.section_cls is ref_cls

    reference = ref_cls.m_def.all_quantities['reference']
    target = reference.type.target_section_def
    assert target.qualified_name() == cls.m_def.qualified_name()

    other = next(c for c, *_ in CASES if c is not cls)
    with pytest.raises(TypeError):
        ref_cls(reference=other(name='wrong type'))


@pytest.mark.parametrize('cls, ref_cls, file_name, name, elements', CASES, ids=IDS)
def test_derived_by_processing(cls, ref_cls, file_name, name, elements):
    precursor = load_precursor(file_name).data

    child = cls(
        name=f'{name}_processed',
        precursors=[ref_cls(reference=precursor)],
        processing=SampleProcessing(
            name='processing',
            steps=[ProcessStep(name='step 1', duration=1800)],
        ),
    )
    archive = EntryArchive(data=child, metadata=EntryMetadata())
    normalize_all(archive)

    assert child.precursors[0].reference.name == name
    assert child.processing.steps[0].name == 'step 1'
    # Elements are taken over from the precursor for search
    assert child.aggregated_elements == elements
    assert archive.results.material.elements == elements
