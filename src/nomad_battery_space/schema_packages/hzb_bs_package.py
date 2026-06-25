#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Battery Components Package

Data model for HZB battery components and sample preparation.

Core components:
- BS_Chemical: Bought-in substances
- ElectrodeMaterial: Synthesized electrode materials
- ElectrodeSheet: Cast electrode sheets
- ElectrolyteStock: Electrolyte solutions
- SeparatorStock: Separator material

Sample components:
- ElectrodeSample: Prepared electrode samples with geometry
- ElectrolyteSample: Prepared electrolyte samples
- SeparatorSample: Prepared separator samples

Base class:
- BatterySample: Base class for all battery types

Geometry support for samples (CircleGeometry, RectangleGeometry, OtherGeometry)
"""

from typing import TYPE_CHECKING

from baseclasses import ProductInfo
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.basesections.v1 import (
    ReadableIdentifiers,
    SynthesisMethod,
)
from nomad.datamodel.metainfo.eln import ELNSubstance
from nomad.metainfo import (
    Enum,
    Quantity,
    Reference,
    SchemaPackage,
    Section,
    SectionProxy,
    SubSection,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from baseclasses.voila import VoilaNotebook

from .utils import (
    collect_and_store_elements,
    create_string_quantity,
    validate_required,
)

m_package = SchemaPackage()


# ============================================================================
# BATCH COMPONENTS (Pre-Assembly)
# ============================================================================

class BS_Chemical(ELNSubstance):
    """
    A chemical substance purchased from a supplier.
    
    This represents the starting material (raw chemical) used as input
    for creating more complex components like electrode materials or
    electrolyte stocks.
    """
    m_def = Section(
        label="HZB Battery: Chemical",
        a_eln={
            "label": "HZB Battery: Chemical",
            "entry_type": "Chemical",
            "properties": {
                "order": [
                    "name",
                    #"creator",
                    "elemental_composition",
                    "pure_substance",
                    "substance_identifiers",
                ],
                "order_default": [
                    "description",
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    # creator = Quantity(
    #     type=CreatorReference,
    #     description='Person who created this initial chemical entry.',
    #     a_eln={
    #         "component": "AuthorEditQuantity",
    #         "label": "creator",
    #     },
    # )

    # pure_substance = SubSection(section_def=PubChemPureSubstanceSectionCustom)

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased chemicals.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)


class BS_ChemicalReference(ArchiveSection):
    """
    Reference to an initial chemical with automatic name resolution.
    
    This section allows referencing an initial chemical substance.
    """
    m_def = Section(
        label_quantity='chemical_name',
        a_eln={
            "label": "Chemical",
            "hide": ["chemical_name"],  
        }
    )

    chemical = Quantity(
        type=Reference(BS_Chemical.m_def),
        description="Reference to the initial chemical substance.",
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "chemical",
            "showSectionLabel": True
        },
    )

    chemical_name = Quantity(
        type=str,
        description="Auto-populated name of the referenced chemical for display in the UI list.",
    )

    role = Quantity(
        type=str,
        description="Role of this chemical in the synthesis or formulation.",
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'solvent',
                    'precursor',
                    'dopant',
                    'binder',
                    'electrolyte salt',
                    'additive',
                    'other',
                ]
            ),
        ),
    )

    volume = Quantity(
        links=['http://purl.obolibrary.org/obo/PATO_0000918', 'https://purl.archive.org/tfsco/TFSCO_00002158'],
        type=float,
        description="Volume of the chemical used.",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "volume",
            "defaultDisplayUnit": "milliliter",
            "units": ["liter", "milliliter", "microliter"],
        },
        unit="milliliter",
    )

    mass = Quantity(
        links=['http://purl.obolibrary.org/obo/PATO_0000125', 'https://purl.archive.org/tfsco/TFSCO_00005020'],
        type=float,
        description="Mass of the chemical used.",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "mass",
            "defaultDisplayUnit": "gram",
            "units": ["gram", "milligram", "microgram"],
        },
        unit="gram",
    )

    concentration_mol = Quantity(
        links=['http://purl.obolibrary.org/obo/PATO_0000033'],
        type=float,
        description="Molar concentration of the chemical (mol per liter).",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "concentration (mol/l)",
            "defaultDisplayUnit": "mol/l",
            "units": ["mol/l", "mmol/l", "mol/ml"],
        },
        unit="mol/l",
    )

    # concentration_mass = Quantity(
    #     links=['http://purl.obolibrary.org/obo/PATO_0000033'],
    #     type=float,
    #     description="Mass concentration of the chemical (mass per volume).",
    #     a_eln={
    #         "component": "NumberEditQuantity",
    #         "label": "concentration (mass)",
    #         "defaultDisplayUnit": "mg/ml",
    #         "units": ["g/l", "mg/ml", "mg/l"],
    #     },
    #     unit="mg/ml",
    # )

    # concentration_vol = Quantity(
    #     links=['http://purl.obolibrary.org/obo/PATO_0000033'],
    #     type=float,
    #     description="Volume-to-volume concentration (v/v), e.g. for liquid additives or solvents.",
    #     a_eln={
    #         "component": "NumberEditQuantity",
    #         "label": "concentration (v/v)",
    #         "defaultDisplayUnit": "%",
    #         "units": ["%", "ul/ml", "ml/l"],
    #     },
    #     unit="dimensionless",
    # )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        # Auto-populate chemical_name from the referenced BS_Chemical's entry metadata
        try:
            if self.chemical:
                if hasattr(self.chemical, 'name') and self.chemical.name:
                    self.chemical_name = self.chemical.name
                elif hasattr(self.chemical, 'entry_metadata') and self.chemical.entry_metadata:
                    try:
                        self.chemical_name = self.chemical.entry_metadata.entry_name
                    except (AttributeError, TypeError):
                        pass
            # Notify parent to re-normalize
            if self.m_parent and hasattr(self.m_parent, 'normalize'):
                self.m_parent.normalize(archive, logger)
        except Exception as e:
            logger.error(f"Error normalizing BS_ChemicalReference: {e}")


class MaterialSynthesisMethodReference(ArchiveSection):
    """
    Reference to a research paper or publication related to material synthesis.
    
    Stores DOI and URL link to the paper.
    """
    
    doi = Quantity(
        type=str,
        description="Digital Object Identifier (DOI) of the publication.",
        a_eln={
            "component": "StringEditQuantity",
            "label": "DOI",
        },
    )
    
    paper_reference = Quantity(
        type=str,
        shape=['*'],
        description="Direct URL link to the research paper or publication.",
        a_eln={
            "component": "URLEditQuantity",
            "label": "paper URL",
        },
    )

# class BS_InstrumentReference(EntityReference):
#     """
#     A section used for referencing an Instrument.
#     """

#     reference = Quantity(
#         type=Instrument,
#         description='A reference to a NOMAD `Instrument` entry.',
#         a_eln=ELNAnnotation(
#             component='ReferenceEditQuantity',
#             label='instrument reference',
#         ),
#     )

class MaterialSynthesisMethod(SynthesisMethod):
    """
    Extended synthesis method for material synthesis with publication references.

    """
    
    m_def = Section(
        a_eln={
            "hide": ["samples"],
            "properties": {
                "order": [
                    "steps",
                    "instruments",
                    "references",
                ],
            },
        }
    )
    
    # instruments = SubSection(
    #     section_def=InstrumentReference,
    #     description="""
    #     A list of all the instruments and their role in this process.
    #     """,
    #     repeats=True,
    # )

    references = SubSection(
        section_def=MaterialSynthesisMethodReference,
        repeats=True,
        description="Publication references related to this synthesis method.",
    )


class ElectrodeMaterial(ELNSubstance):    
    """
    Synthesized electrode material.
    
    This represents the electrode material created through a synthesis process
    for use in the battery. It includes references to
    initial chemicals used as inputs, composition information, and synthesis
    methodology details.
    """
    m_def = Section(
        label="HZB Battery: Electrode Material",
        a_eln={
            "label": "HZB Battery: Electrode Material",
            "entry_type": "ElectrodeMaterial",
            #"hide": ['pure_substance', 'substance_identifiers'],
            "properties": {
                "order": [
                    "name",
                    "creator",
                    "chemical_composition_or_formulas",
                    "synthesis",
                    "yield_percent",
                    "description",
                    "volume_and_weights",
                    "elemental_composition",
                    "pure_substance",
                    "chemicals",
                ],
                "order_default": [
                    "substance_identifiers",
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    chemical_composition_or_formulas = create_string_quantity(
        "chemical composition/formula",
        description="Chemical composition or formula of the synthesized electrode material (e.g., LiCoO2, NCA, etc.).",
    )

    chemicals = SubSection(
        section_def=BS_ChemicalReference,
        repeats=True,
        description="References to the chemical substances used as input materials for synthesizing this electrode material.",
        a_eln={
            "label": "chemicals",
            "showSectionLabel": True,
        },
    )

    synthesis = SubSection(
        section_def=MaterialSynthesisMethod,
        description="Detailed synthesis methodology including steps, instruments, timing, and publication references.",
    )

    yield_percent = Quantity(
        type=float,
        description="Synthesis yield percentage.",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "yield",
            "defaultDisplayUnit": "%",
            "props": {"minValue": 0, "maxValue": 100},
        },
        unit="dimensionless",
    )

    volume_and_weights = SubSection(
        section_def=SectionProxy('VolumeAndWeights'),
        description="Volume and mass information for the synthesized electrode material.",
        a_eln={
            "label": "volume and weights",
        },
    )

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased electrode materials.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description='Chemical elements aggregated from all referenced components for NOMAD search.',
        a_eln={
            "label": "aggregated elements",
        }
    )

    #TODO: Let user decide whether to use PubChem substance like below or keep it flexible with the dropdown selection
    # 1) pure_substance = SubSection(section_def=PubChemPureSubstanceSectionCustom)
    # 2) creator needed?

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        
        # Normalize all referenced chemicals to ensure fresh data
        if self.chemicals:
            for chem_ref in self.chemicals:
                if chem_ref.chemical:
                    chem_ref.chemical.normalize(archive, logger)
        
        # Collect and store elements from all sources
        collect_and_store_elements(self, archive, chemicals=self.chemicals)


class ActiveMaterialComponent(ArchiveSection):
    """
    A component material in an electrode sheet.
    
    This section represents an active material (e.g., cathode material, binder, current collector)
    that is part of the electrode sheet, with its role and mass contribution.
    """
    m_def = Section(
        label_quantity='material_name',
        a_eln={
            "hide": ["material_name"],
        }
    )

    material = Quantity(
        type=Reference(ElectrodeMaterial.m_def),
        description="Reference to the electrode material used in this component.",
        a_eln={"component": "ReferenceEditQuantity", 
               "label": "material",
               "showSectionLabel": True,
               },
    )

    material_name = Quantity(
        type=str,
        description="Auto-populated name of the referenced electrode material for display in the UI list."
    )

    role = Quantity(
        type=str,
        description="Role of this material in the sheet (e.g., active material, binder, current collector, additive).",
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'current collector',
                    'binder',
                    'active material',
                    'additive',
                    'conductive agent',
                ]
            ),
        ),
    )

    mass = Quantity(
        type=float,
        description="Mass of this material component in the sheet.",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "mass",
            "defaultDisplayUnit": "milligram",
            "units": ["gram", "milligram", "microgram"],
        },
        unit="milligram",
    )

    wt_percent = Quantity(
        type=float,
        description="Weight percent (wt%) of this material component in the electrode sheet.",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "wt%",
            "defaultDisplayUnit": "%",
            "props": {"minValue": 0, "maxValue": 100},
        },
        unit="dimensionless",
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        # Auto-populate material_name from the referenced ElectrodeMaterial
        try:
            if self.material:
                if hasattr(self.material, 'name') and self.material.name:
                    self.material_name = self.material.name
                elif hasattr(self.material, 'entry_metadata') and self.material.entry_metadata:
                    try:
                        self.material_name = self.material.entry_metadata.entry_name
                    except (AttributeError, TypeError):
                        pass
            # Notify parent to re-normalize
            if self.m_parent and hasattr(self.m_parent, 'normalize'):
                self.m_parent.normalize(archive, logger)
        except Exception as e:
            logger.error(f"Error normalizing ActiveMaterialComponent: {e}")


class ElectrodeSheet(ELNSubstance):
    """
    Cast electrode sheet for battery assembly.
    
    Represents a prepared electrode sheet created through coating/casting.
    Includes multiple active material components (active material, binders, 
    current collectors, additives) with their individual roles and masses.
    """
    m_def = Section(
        label="HZB Battery: Electrode Sheet",
        a_eln={
            "label": "HZB Battery: Electrode Sheet",
            "entry_type": "ElectrodeSheet",
            "hide": ['pure_substance', 'elemental_composition'], 
            "properties": {
                "order": [
                    "name",
                    "casting_procedure",
                    "dimensions_and_weights",
                    "chemicals",
                    "electrode_materials",           
                ],
                "order_default": [
                    "description",
                    "substance_identifiers",
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    casting_procedure = create_string_quantity(
        "casting procedure (drop-down???)",
        description="Procedure used to cast the electrode sheet (e.g., dropcast, spray coating, etc.).",
    )

    electrode_materials = SubSection(
        section_def=ActiveMaterialComponent,
        repeats=True,
        description="Components (active materials, binders, current collectors, additives) that make up the electrode sheet.",
        a_eln={
            "label": "electrode materials",
        },
    )

    chemicals = SubSection(
        section_def=BS_ChemicalReference,
        repeats=True,
        description="References to initial chemical substances used as input materials for this electrode sheet.",
        a_eln={
            "label": "chemicals",
            "showSectionLabel": True,
        },
    )

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased electrode sheets.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    dimensions_and_weights = SubSection(
        section_def=SectionProxy('DimensionsAndWeights'),
        description="Geometric surface area and mass information for the electrode sheet.",
        a_eln={
            "label": "dimensions and weights",
        },
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description='Chemical elements aggregated from all referenced components for NOMAD search.',
        a_eln={
            "label": "aggregated elements",
        }
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        
        # Normalize all referenced materials and chemicals to ensure fresh data
        if self.electrode_materials:
            for mat_component in self.electrode_materials:
                if mat_component.material:
                    mat_component.material.normalize(archive, logger)
        
        if self.chemicals:
            for chem_ref in self.chemicals:
                if chem_ref.chemical:
                    chem_ref.chemical.normalize(archive, logger)
        
        # Collect and store elements from all sources
        collect_and_store_elements(self, archive, materials=self.electrode_materials, chemicals=self.chemicals)


class ElectrolyteStock(ELNSubstance):
    """
    Electrolyte stock solution.
    
    Extends the baseclasses Electrolyte with stock/batch specific information.
    Contains salts and solvents mixed together for use in battery assembly.
    Tracks state (liquid/solid) and volume.
    """
    m_def = Section(
        links=['https://w3id.org/emmo/domain/electrochemistry#electrochemistry_fb0d9eef_92af_4628_8814_e065ca255d59'],
        label="HZB Battery: Electrolyte Stock",
        a_eln={
            "label": "HZB Battery: Electrolyte Stock",
            "entry_type": "ElectrolyteStock",
            "hide": ['pure_substance', 'elemental_composition'],
            "properties": {
                "order": [
                    "name",
                    "state",
                    "volume_and_weights",
                    "chemicals",
                ],
                "order_default": [
                    "description",
                    "substance_identifiers",
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    StateEnum = Enum(["Liquid", "Solid"])
    state = Quantity(
        type=StateEnum,
        default='Liquid',
        description="Physical state of the electrolyte stock.",
        a_eln={
            "component": "EnumEditQuantity",
            "label": "state",
        }
    )

    chemicals = SubSection(
        section_def=BS_ChemicalReference,
        repeats=True,
        description="References to initial chemical substances used as input materials for this electrolyte stock.",
        a_eln={
            "label": "chemicals",
            "showSectionLabel": True,
        },
    )

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased electrolyte stocks.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    volume_and_weights = SubSection(
        section_def=SectionProxy('VolumeAndWeights'),
        description="Volume and mass information for the electrolyte stock.",
        a_eln={
            "label": "volume and weights",
        },
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description=(
            'Chemical elements aggregated from all referenced components for NOMAD search.'
        ),
        a_eln={
            "label": "aggregated elements",
        }
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        
        # Normalize all referenced chemicals to ensure fresh data
        if self.chemicals:
            for chem_ref in self.chemicals:
                if chem_ref.chemical:
                    chem_ref.chemical.normalize(archive, logger)
        
        # Collect and store elements from all sources
        collect_and_store_elements(self, archive, chemicals=self.chemicals)


class SeparatorStock(ELNSubstance):
    """
    Separator material stock.
    
    Represents a sheet of separator material (e.g., porous polymer,
    ceramic coating) used to separate anode and cathode in the battery.
    """
    m_def = Section(
        links=['https://w3id.org/emmo/domain/electrochemistry#electrochemistry_331e6cca_f260_4bf8_af55_35304fe1bbe0'],
        label="HZB Battery: Separator Stock",
        a_eln={
            "label": "HZB Battery: Separator Stock",
            "entry_type": "SeparatorStock",
            "hide": ['pure_substance', 'elemental_composition'],
            "properties": {
                "order": [
                    "name",
                    "dimensions_and_weights",
                    "chemicals",
                ],
                "order_default": [
                    "description",
                    "substance_identifiers",
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    chemicals = SubSection(
        section_def=BS_ChemicalReference,
        repeats=True,
        description="References to initial chemical substances used as input materials for this separator stock.",
        a_eln={
            "label": "chemicals",
            "showSectionLabel": True,
        },
    )

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased separator stocks.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    # porosity = Quantity(
    #     type=float,
    #     description="Porosity percentage of the separator",
    #     a_eln={
    #         "component": "NumberEditQuantity",
    #         "label": "porosity",
    #         "defaultDisplayUnit": "%",
    #         "props": {"minValue": 0, "maxValue": 100},
    #     },
    #     unit="dimensionless",
    # )

    dimensions_and_weights = SubSection(
        section_def=SectionProxy('DimensionsAndWeights'),
        description="Thickness and geometric dimensions of the separator stock.",
        a_eln={
            "label": "Dimensions and Weights",
        },
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description='Chemical elements aggregated from all referenced components for NOMAD search.',
        a_eln={
            "label": "aggregated elements",
        }
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        
        # Normalize all referenced chemicals to ensure fresh data
        if self.chemicals:
            for chem_ref in self.chemicals:
                if chem_ref.chemical:
                    chem_ref.chemical.normalize(archive, logger)
        
        # Collect and store elements from all sources
        collect_and_store_elements(self, archive, chemicals=self.chemicals)


# ============================================================================
# SAMPLE COMPONENTS (Cut/Prepared from Batch)
# ============================================================================

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
    
    def derive_area(self):
        if self.diameter is not None:
            return 3.14159 * (self.diameter / 2) ** 2
        return None
    
    area = Quantity(
        type=float,
        unit="centimeter**2",
        description="Calculated area of the circular sample.",
        #derived=derive_area,
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
    
    def derive_area(self):
        if self.length is not None and self.width is not None:
            return self.length * self.width
        return None
    
    area = Quantity(
        type=float,
        unit="centimeter**2",
        description="Calculated area of the rectangular sample in cm².",
        #derived=derive_area,
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


# ============================================================================
# COMPOSITE SUBSECTIONS FOR DIMENSIONS, WEIGHT, AND VOLUME
# ============================================================================

class DimensionsAndWeights(ArchiveSection):
    """
    Composite subsection combining thickness, mass, and shape information for solid materials.
    
    """
    
    m_def = Section(
        label='dimensions and weights',
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
            "units": ["gram", "milligram", "microgram"],
        },
    )
    
    shape = SubSection(
        section_def=SectionProxy('GeometricalShape'),
        description="Geometric shape and dimensions of the material."
    )


class VolumeAndWeights(ArchiveSection):
    """
    Composite subsection combining mass and volume information for materials and liquids.

    """
    
    m_def = Section(
        label='volume and weights',
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
            "units": ["gram", "milligram", "microgram"],
        },
    )
    
    
class ElectrodeSample(ELNSubstance):
    """
    Prepared electrode sample for battery assembly.
    
    This is a cut/prepared sample from an ElectrodeSheet with specific
    dimensions and properties for use in the battery assembly.
    The geometry subsection supports multiple shape types (Circle, Rectangle, Other).
    """
    m_def = Section(
        label="HZB Battery: Electrode Sample",
        a_eln={
            "label": "HZB Battery: Electrode Sample",
            "entry_type": "ElectrodeSample",
            "hide": ['pure_substance', 'elemental_composition'],
            "properties": {
                "order": [
                    "name",
                    "electrode_sheet",
                    "dimensions_and_weights",
                    "chemicals",
                ],
                "order_default": [
                    "description",
                    "substance_identifiers",
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    electrode_sheet = Quantity(
        type=Reference(ElectrodeSheet.m_def),
        description="Reference to the electrode sheet this sample comes from.",
        a_eln={
                "component": "ReferenceEditQuantity",
                "showSectionLabel": True,
               },
    )

    dimensions_and_weights = SubSection(
        section_def=SectionProxy('DimensionsAndWeights'),
        description="Geometric shape, dimensions and mass information for the electrode sample.",
        a_eln={            
            "label": "dimensions and weights",
        },
    )

    chemicals = SubSection(
        section_def=BS_ChemicalReference,
        repeats=True,
        description="References to chemical substances used as input materials for this electrode sample.",
        a_eln={
            "label": "chemicals",
            "showSectionLabel": True,
        },
    )

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased electrode samples.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description='Chemical elements aggregated from all referenced components for NOMAD search.',
        a_eln={
            "label": "aggregated elements",
        }
    )    
        
    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        
        # Parent-override: Copy thickness from parent sheet
        if self.electrode_sheet and self.electrode_sheet.dimensions_and_weights:
            if not self.dimensions_and_weights:
                self.dimensions_and_weights = DimensionsAndWeights()
            if self.electrode_sheet.dimensions_and_weights.thickness:
                self.dimensions_and_weights.thickness = self.electrode_sheet.dimensions_and_weights.thickness
        
        # Normalize referenced components
        if self.electrode_sheet:
            self.electrode_sheet.normalize(archive, logger)
        if self.chemicals:
            for chem_ref in self.chemicals:
                if chem_ref.chemical:
                    chem_ref.chemical.normalize(archive, logger)
        
        # Collect and store elements from all sources
        collect_and_store_elements(self, archive, chemicals=self.chemicals, referenced_components=[self.electrode_sheet])


class ElectrolyteSample(ELNSubstance):
    """
    Prepared electrolyte sample for battery assembly.
    
    This is a measured amount of electrolyte from the ElectrolyteStock
    for use in a specific battery cell.
    """
    m_def = Section(
        label="HZB Battery: Electrolyte Sample",
        a_eln={
            "label": "HZB Battery: Electrolyte Sample",
            "hide": ['elemental_composition', 'pure_substance'],
            "properties": {
                "order": [
                    "name",
                    "electrolyte_stock",
                    "volume_and_weights",
                ],
                "order_default": [
                    "description",
                    "substance_identifiers",
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    electrolyte_stock = Quantity(
        type=Reference(ElectrolyteStock.m_def),
        description="Reference to the electrolyte stock this sample comes from.",
        a_eln={
                "component": "ReferenceEditQuantity",
                "showSectionLabel": True,
               },
    )

    volume_and_weights = SubSection(
        section_def=SectionProxy('VolumeAndWeights'),
        description="Volume and mass information for the electrolyte sample.",
        a_eln={
            "label": "volume and weights",
        },
    )

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased electrolyte samples.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description='Chemical elements aggregated from all referenced components for NOMAD search.',
        a_eln={
            "label": "aggregated elements",
        }
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        
        # Normalize referenced electrolyte_stock
        if self.electrolyte_stock:
            self.electrolyte_stock.normalize(archive, logger)
        
        # Collect and store elements from all sources
        collect_and_store_elements(self, archive, referenced_components=[self.electrolyte_stock])


class SeparatorSample(ELNSubstance):
    """
    Prepared separator sample for battery assembly.
    
    This is a cut sample from the SeparatorStock for use in a specific
    battery cell assembly.
    """
    m_def = Section(
        label="HZB Battery: Separator Sample",
        a_eln={
            "label": "HZB Battery: Separator Sample",
            "hide": ['elemental_composition', 'pure_substance'],
            "properties": {
                "order": [
                    "name",
                    "separator_stock",
                    "dimensions_and_weights",
                ],
                "order_default": [
                    "description",
                    "substance_identifiers",
                ]
            },            
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    separator_stock = Quantity(
        type=Reference(SeparatorStock.m_def),
        description="Reference to the separator stock this sample comes from.",
        a_eln={
            "component": "ReferenceEditQuantity",
            "showSectionLabel": True,
        },
    )

    dimensions_and_weights = SubSection(
        section_def=SectionProxy('DimensionsAndWeights'),
        description="Thickness and geometric dimensions of the separator sample.",
        a_eln={
            "label": "Dimensions and Weights",
        },
    )

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased separator samples.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description='Chemical elements aggregated from all referenced components for NOMAD search.',
        a_eln={
            "label": "aggregated elements",
        }
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        
        # Parent-override: Copy thickness from parent stock
        if self.separator_stock and self.separator_stock.dimensions_and_weights:
            if not self.dimensions_and_weights:
                self.dimensions_and_weights = DimensionsAndWeights()
            if self.separator_stock.dimensions_and_weights.thickness:
                self.dimensions_and_weights.thickness = self.separator_stock.dimensions_and_weights.thickness
        
        # Normalize referenced components
        if self.separator_stock:
            self.separator_stock.normalize(archive, logger)
        
        # Collect and store elements from all sources
        collect_and_store_elements(self, archive, referenced_components=[self.separator_stock])


# ============================================================================
# BASE BATTERY SAMPLE
# ============================================================================

class BatterySample(ELNSubstance):
    '''
    Base class for battery samples - provides common fields for all battery types.
    
    This is a generalized battery entry that serves as the base for specific
    battery implementations (e.g., CoinCellBattery). 
    '''
    m_def = Section(
        links=['https://w3id.org/emmo/domain/battery#battery_68ed592a_7924_45d0_a108_94d6275d57f0'],
        label="HZB Battery: Generic Sample",
        a_eln={
            "label": "HZB Battery: Generic Sample",
            "entry_type": "BatterySample",
            "hide": ['pure_substance', 
                     'elemental_composition'],  
            "properties": {
                "order": [
                    "lab_id",
                    "name",
                    "datetime",
                    "working_electrode",
                    "counter_electrode",
                    "reference_electrode",
                    "separator",
                    "electrolyte",
                    "procedure_sketch",
                    "aggregated_elements",
                    "product_info"
                ],
                "order_default": [
                    "description",
                    "substance_identifiers", 
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    substance_identifiers = SubSection(
        section_def=ReadableIdentifiers,
        a_eln=dict(label='sample identifiers')
    )
    lab_id = Quantity(
        type=str,
        description="""
        A human readable battery ID that is at least unique for the lab.
        """,
        a_eln=dict(component='StringEditQuantity', label='battery ID', required=True),
    )

    name = Quantity(
        type=str,
        description='The name of the battery entry.',
        a_eln=dict(component='StringEditQuantity', label='battery name', required=True),
    )

    description = Quantity(
        type=str,
        description="""
        A field for adding additional information about the battery that is not captured
        by the other quantities and subsections.
        """,
        a_eln=dict(
            component='RichTextEditQuantity',
            label='detailed battery description',
            props={"height": 200}, required=False
        ),
    )

    procedure_sketch = Quantity(
        type=str,
        description="Photo or PDF file showing the assembly procedure sketch or technical drawing that documents the battery assembly steps and configuration.",
        a_eln={"component": "FileEditQuantity"}
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description='Chemical elements aggregated from all referenced components for NOMAD search.',
        a_eln={
            "label": "aggregated elements",
        }
    )

    product_info = SubSection(
        section_def=ProductInfo,
        description="Product information for supplier/commercially purchased batteries or battery assemblies.",
        a_eln={
            "label": "product info / supplier",
        },
    )

    # ---- Battery Components ----

    working_electrode = Quantity(
        type=Reference(ElectrodeSample.m_def),
        description="The working electrode sample used in the battery (negative or positive depending on setup).",
        a_eln={"component": "ReferenceEditQuantity", "showSectionLabel": True},
    )

    counter_electrode = Quantity(
        type=Reference(ElectrodeSample.m_def),
        description="The counter/auxiliary electrode sample used in the battery (opposite polarity to the working electrode).",
        a_eln={"component": "ReferenceEditQuantity", "showSectionLabel": True},
    )

    reference_electrode = Quantity(
        type=Reference(ElectrodeSample.m_def),
        description="Reference electrode for three-electrode setup (optional).",
        a_eln={"component": "ReferenceEditQuantity", "showSectionLabel": True},
    )

    separator = Quantity(
        type=Reference(SeparatorSample.m_def),
        description="The separator sample separating anode and cathode.",
        a_eln={"component": "ReferenceEditQuantity", "showSectionLabel": True},
    )

    electrolyte = Quantity(
        type=Reference(ElectrolyteSample.m_def),
        description="The electrolyte sample used in the battery.",
        a_eln={"component": "ReferenceEditQuantity", "showSectionLabel": True},
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        # Normalize all referenced battery components to ensure fresh data
        if self.working_electrode:
            self.working_electrode.normalize(archive, logger)
        if self.counter_electrode:
            self.counter_electrode.normalize(archive, logger)
        if self.reference_electrode:
            self.reference_electrode.normalize(archive, logger)
        if self.separator:
            self.separator.normalize(archive, logger)
        if self.electrolyte:
            self.electrolyte.normalize(archive, logger)

        # Validate required lab/battery id
        validate_required(self.lab_id, name='battery ID')

        # Collect and store elements from all referenced components
        referenced_components = [
            self.working_electrode,
            self.counter_electrode,
            self.reference_electrode,
            self.separator,
            self.electrolyte,
        ]
        collect_and_store_elements(self, archive, referenced_components=referenced_components)


# ============================================================================
# VOILA NOTEBOOK (for battery batch sample uploads)
# ============================================================================

class BS_VoilaNotebook(VoilaNotebook, EntryData):

    m_def = Section(a_eln=dict(hide=['lab_id']))

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


m_package.__init_metainfo__()
