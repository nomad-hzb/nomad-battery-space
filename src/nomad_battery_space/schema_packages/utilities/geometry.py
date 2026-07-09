from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity, Section


class GeometricalShape(ArchiveSection):
    """Base class for sample geometry."""
    
    m_def = Section(
        label='Select shape from the dropdown',
    )


class CircleGeometry(GeometricalShape):
    """Circular sample geometry with diameter."""
    
    m_def = Section(
        label='Circle',
    )
    
    diameter = Quantity(
        type=float,
        description="Diameter of the circular sample.",
        unit="millimeter",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "diameter",
            "defaultDisplayUnit": "millimeter",
        },
    )
    area = Quantity(
        type=float,
        unit="centimeter**2",
        description="Calculated area of the circular sample.",
        a_eln={
            "label": "area",
            "defaultDisplayUnit": "centimeter**2",
        },
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if self.diameter is not None:
            self.area = 3.14159 * (self.diameter / 2) ** 2


class RectangleGeometry(GeometricalShape):
    """Rectangular sample geometry with length and width."""
    
    m_def = Section(
        label='Rectangle',
    )
    
    length = Quantity(
        type=float,
        description="Length of the rectangular sample.",
        unit="millimeter",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "length",
            "defaultDisplayUnit": "millimeter",
        },
    )
    width = Quantity(
        type=float,
        description="Width of the rectangular sample.",
        unit="millimeter",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "width",
            "defaultDisplayUnit": "millimeter",
        },
    )
    area = Quantity(
        type=float,
        unit="centimeter**2",
        description="Calculated area of the rectangular sample in cm².",
        a_eln={
            "label": "area",
            "defaultDisplayUnit": "centimeter**2",
        },
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if self.length is not None and self.width is not None:
            self.area = self.length * self.width


class OtherGeometry(GeometricalShape):
    """Other/custom sample geometry with free text description."""
    
    m_def = Section(
        label='Other',
    )
    
    description = Quantity(
        type=str,
        description="Free text description of the sample geometry.",
        a_eln={
            "component": "StringEditQuantity",
            "label": "shape description",
        },
    )
