from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

from .geometry import GeometricalShape

m_package = SchemaPackage()


class DimensionsAndWeights(ArchiveSection):
    """
    Composite subsection combining thickness, mass, and shape information for solid materials.
    """

    m_def = Section(
        label='Dimensions and Weights',
    )

    thickness = Quantity(
        type=float,
        description='Thickness of the solid material.',
        unit='micrometer',
        a_eln={
            'component': 'NumberEditQuantity',
            'label': 'thickness',
            'defaultDisplayUnit': 'micrometer',
        },
    )
    mass = Quantity(
        type=float,
        description='Mass of the material.',
        unit='gram',
        a_eln={
            'component': 'NumberEditQuantity',
            'label': 'mass',
            'defaultDisplayUnit': 'gram',
        },
    )
    shape = SubSection(
        section_def=GeometricalShape,
        description='Geometric shape and dimensions of the material.',
    )


class VolumeAndWeights(ArchiveSection):
    """
    Composite subsection combining mass and volume information for materials and liquids.
    """

    m_def = Section(
        label='Volume and Weights',
    )

    volume = Quantity(
        type=float,
        description='Volume of the material or solution.',
        unit='milliliter',
        a_eln={
            'component': 'NumberEditQuantity',
            'label': 'volume',
            'defaultDisplayUnit': 'milliliter',
        },
    )
    mass = Quantity(
        type=float,
        description='Mass of the material or solution.',
        unit='gram',
        a_eln={
            'component': 'NumberEditQuantity',
            'label': 'mass',
            'defaultDisplayUnit': 'gram',
        },
    )


# ============================================================================
# PACKAGE INITIALIZATION
# ============================================================================

m_package.__init_metainfo__()
