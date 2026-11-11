from nomad.client import normalize_all
from nomad.datamodel import EntryArchive, EntryMetadata
from nomad.datamodel.metainfo.basesections.v1 import ElementalComposition

from nomad_battery_space.schema_packages.hzb_bs_assembly_package import (
    CoinCellBattery,
)
from nomad_battery_space.schema_packages.hzb_bs_package import (
    ActiveMaterialComponent,
    BS_Chemical,
    BS_ChemicalReference,
    ElectrodeMaterial,
    ElectrodeSample,
    ElectrodeSheet,
    ElectrolyteSample,
    ElectrolyteStock,
    SeparatorSample,
    SeparatorStock,
)


def composition(*elements):
    return [ElementalComposition(element=element) for element in elements]


def test_elements_are_aggregated_along_the_chain():
    """Elements entered at chemical and stock level reach the assembled cell."""
    lithium_salt = BS_Chemical(
        name='LiPF6', elemental_composition=composition('Li', 'P', 'F')
    )
    nmc = ElectrodeMaterial(
        name='NMC111', elemental_composition=composition('Ni', 'Mn', 'Co')
    )
    sheet = ElectrodeSheet(
        name='NMC111_sheet',
        electrode_materials=[
            ActiveMaterialComponent(material=nmc, role='active material')
        ],
    )
    electrolyte = ElectrolyteStock(
        name='LP30', chemicals=[BS_ChemicalReference(chemical=lithium_salt)]
    )
    separator = SeparatorStock(
        name='Celgard_2400', elemental_composition=composition('C', 'H')
    )

    cell = CoinCellBattery(
        lab_id='CC_001',
        name='coin_cell_01',
        working_electrode=ElectrodeSample(name='disc_01', electrode_sheet=sheet),
        electrolyte=ElectrolyteSample(
            name='LP30_cell_01', electrolyte_stock=electrolyte
        ),
        separator=SeparatorSample(name='separator_01', separator_stock=separator),
    )
    archive = EntryArchive(data=cell, metadata=EntryMetadata())
    normalize_all(archive)

    expected = ['C', 'Co', 'F', 'H', 'Li', 'Mn', 'Ni', 'P']
    assert cell.aggregated_elements == expected
    assert archive.results.material.elements == expected
