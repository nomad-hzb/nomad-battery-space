from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity, SubSection
from nomad.metainfo.metainfo import Section

from .geometry import GeometricalShape


class DimensionsAndWeights(ArchiveSection):
    """
    Composite subsection combining thickness, mass, and shape information for solid materials.
    """
    
    m_def = Section(
        label='Dimensions and Weights',
    )
    
    thickness = Quantity(
        type=float,
        description="Thickness of the solid material.",
        unit="micrometer",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "thickness",
            "defaultDisplayUnit": "micrometer",
        },
    )
    mass = Quantity(
        type=float,
        description="Mass of the material.",
        unit="gram",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "mass",
            "defaultDisplayUnit": "gram",
        },
    )
    shape = SubSection(
        section_def=GeometricalShape,
        description="Geometric shape and dimensions of the material."
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
        description="Volume of the material or solution.",
        unit="milliliter",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "volume",
            "defaultDisplayUnit": "milliliter",
        },
    )
    mass = Quantity(
        type=float,
        description="Mass of the material or solution.",
        unit="gram",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "mass",
            "defaultDisplayUnit": "gram",
        },
    )
