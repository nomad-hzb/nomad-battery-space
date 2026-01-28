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

from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.basesections.v1 import (
    EntityReference,
)
from nomad.datamodel.metainfo.eln import (
    ELNSubstance,
    SampleID,
)
from nomad.datamodel.results import (
    Material,
    Results,
)
from nomad.metainfo import (
    Enum,
    Quantity,
    Reference,
    SchemaPackage,
    Section,
    SubSection,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )
from .utils import validate_required

m_package = SchemaPackage()

class Anode(ELNSubstance):
    '''
    An anode entry in the battery schema.
    '''    
    m_def = Section(
        links=['https://w3id.org/emmo/domain/electrochemistry#electrochemistry_b6319c74_d2ce_48c0_a75a_63156776b302'],
        label="HZB Battery: Anode",
        a_eln={
            "label": "Anode",
            "entry_type": "Anode",
            "hide": ['pure_substance', 'substance_identifiers'],
            "properties": {
                "order": [
                    "name", 
                    "mass",
                    "area",
                ],
                "order_default": [
                    "description"
                ]
            },
        }
    )
    
    mass = Quantity(
        type=float,
        description='Total mass of the anode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Mass",
            "defaultDisplayUnit": "gram"
        },
        unit="gram",
    )

    area = Quantity(
        type=float,
        description='Geometric surface area of the anode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Area",
            "defaultDisplayUnit": "centimeter ** 2"
        },
        unit='centimeter ** 2',
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `Anode` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)

class Cathode(ELNSubstance):
    '''
    A Cathode entry in the battery schema.
    '''
    m_def = Section(
        links=['https://w3id.org/emmo/domain/electrochemistry#electrochemistry_35c650ab_3b23_4938_b312_1b0dede2e6d5'],
        label="HZB Battery: Cathode",
        a_eln={
            "label": "Cathode",
            "entry_type": "Cathode",
            "hide": ['pure_substance', 'substance_identifiers'],
            "properties": {
                "order": [
                    "name", 
                    "mass",
                    "area",
                    "mass_active_material",
                ],
                "order_default": [
                    "description"
                ]
            },
        }
    )
    
    mass = Quantity(
        type=float,
        description='Total mass of the cathode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Mass",
            "defaultDisplayUnit": "gram"
        },
        unit="gram",
    )
    area = Quantity(
        type=float,
        description='Geometric surface area of the cathode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Area",
            "defaultDisplayUnit": "centimeter ** 2"
        },
        unit='centimeter ** 2',
    )
    mass_active_material = Quantity(
        type=float,
        description='Mass of the active material in the cathode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Mass of active material",
            "defaultDisplayUnit": "%"
        },
        unit="dimensionless",
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `Cathode` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)


class Electrolyte(ELNSubstance):
    '''
    An Electrolyte entry in the battery schema.
    '''
    m_def = Section(
        links=['https://w3id.org/emmo/domain/electrochemistry#electrochemistry_fb0d9eef_92af_4628_8814_e065ca255d59'],
        label="HZB Battery: Electrolyte",
        a_eln={
            "properties": {
                "order": [
                    "state", 
                    "name",                   
                    "volume",
                    "mass",
                ],
                "order_default": [
                    "description"
                ]
            },
            "label": "Electrolyte",
            "entry_type": "Electrolyte",
            "hide": ['pure_substance', 'substance_identifiers'],
        },
    )

    StateEnum = Enum(["Liquid", "Solid"])
    state = Quantity(
        type=StateEnum,
        description='Physical state of the electrolyte.',
        a_eln={
            "component": "EnumEditQuantity",
            "label": "State",
        }
    )
    mass = Quantity(
        type=float,
        description='Total mass of the electrolyte.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Mass",
            "defaultDisplayUnit": "gram",
            "units": ["gram", "milligram", "microgram"],
        },
        unit="gram",
    )

    volume = Quantity(
        type=float,
        description='Volume of the electrolyte.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Volume",
            "defaultDisplayUnit": "milliliter",
            "units": ["liter", "milliliter", "microliter"],
        },
        unit="milliliter",
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `Electrolyte` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)


class Separator(ELNSubstance):
    '''
    A Separator entry in the battery schema.
    '''
    m_def = Section(
        links=['https://w3id.org/emmo/domain/electrochemistry#electrochemistry_331e6cca_f260_4bf8_af55_35304fe1bbe0'],
        label="HZB Battery: Separator",
        a_eln={
            "properties": {
                "order": [
                    "name",
                    "thickness"
                ]
            },
            "label": "Separator",
            "entry_type": "Separator",
            "hide": ['pure_substance', 'substance_identifiers'],
        },
    )
    
    thickness = Quantity(
        type=float,
        description='Thickness of the separator.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "thickness",
            "defaultDisplayUnit": "micrometer"
        },
        unit="micrometer",
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `Separator` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)


class AnodeReference(EntityReference):
    """
    A section used for referencing an Anode into a Battery.
    """

    reference = Quantity(
        type=Anode,
        description='A reference to a Battery `Anode` entry.',
        a_eln={
            "component": 'ReferenceEditQuantity',
            "label": 'Anode',
        },
    )


class Components(ArchiveSection):
    '''
    Pure UI grouping container inside BatterySample.
    '''
    m_def = Section(
        a_eln={
            "properties": {
                "order": [
                    "anode",
                    "cathode",
                    "electrolyte",
                    "separator"
                ]
            }
        },
        label="Components",)
    anode_q = Quantity(
        type=Reference(Anode),
        description='Reference to an Anode entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Anode"
        },
    )
    cathode_q = Quantity(
        type=Reference(Cathode),
        description='Reference to a Cathode entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Cathode"
        },
    )
    electrolyte_q = Quantity(
        type=Reference(Electrolyte),
        description='Reference to a Electrolyte entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Electrolyte"
        },
    )
    separator_q = Quantity(
        type=Reference(Separator),
        description='Reference to a Separator entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Separator"
        },
    )


class BatterySample(ELNSubstance):
    '''
    Basic information about a battery sample including its components.
    '''
    m_def = Section(
        links=['https://w3id.org/emmo/domain/battery#battery_68ed592a_7924_45d0_a108_94d6275d57f0'],
        label="HZB Battery Sample",
        a_eln={
            "properties": {
                "order": [
                    "lab_id",
                    "name",
                    "datetime",
                    "description",
                    "tags",
                    "components",
                ]
            },
            "label": "HZB Battery",
            "entry_type": "Battery Sample",
            "hide": ['pure_substance', 
                     'substance_identifiers', 
                     'elemental_composition',
                     'sample_identifiers'],  
        },
    )

    name = Quantity(
        type=str,
        description='The name of the battery entry.',
        a_eln=dict(component='StringEditQuantity', label='battery name', required=True),
    )
    lab_id = Quantity(
        type=str,
        description="""
        A human readable battery ID that is at least unique for the lab.
        """,
        a_eln=dict(component='StringEditQuantity', label='battery ID', required=True),
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
            props={"height": 200}, required=True
        ),
    )
    
    components = SubSection(
        section_def=Components,
    )
    sample_identifiers = SubSection(
        section_def=SampleID,
    )

    aggregated_elements = Quantity(
        type=str,
        shape=['*'],
        description=(
            'All chemical elements found in referenced components '
            '(anode, cathode, electrolyte, etc.), used for search.'
        ),
        a_eln={
            "label": "aggregated elements",
        }
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `BatterySample` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)

        # Validate required lab/battery id
        validate_required(self.lab_id, name='battery ID')

        elements = set()

        def extract_elements(component):
            if component is None:
                return
            ec_list = getattr(component, 'elemental_composition', None)
            if not ec_list:
                return
            for comp in ec_list:
                el = getattr(comp, 'element', None)
                if el:
                    elements.add(str(el))

        extract_elements(getattr(self.components, 'anode_q', None))
        extract_elements(getattr(self.components, 'cathode_q', None))
        extract_elements(getattr(self.components, 'electrolyte_q', None))
        extract_elements(getattr(self.components, 'separator_q', None))

        elements_list = sorted(elements)

        # Save into aggregated field
        self.aggregated_elements = elements_list

        if archive.results is None:
            archive.results = Results()

        if archive.results.material is None:
            archive.results.material = Material()


        archive.results.material.elements = elements_list
        

class CoinCellBattery(BatterySample):
    m_def = Section(
        links=['https://w3id.org/emmo/domain/battery#battery_b7fdab58_6e91_4c84_b097_b06eff86a124'],
        label="HZB Coin Cell Battery",
        a_eln={
            "label": "HZB Coin Cell Battery",
            "entry_type": "Coin Cell",
            "properties": {
                "order": [
                    "lab_id",
                    "name",
                    "datetime",
                    "case_id",
                    "case_crimp",
                    "pressure",
                    "description",
                    "tags",
                    "components",
                ]
            },
             "hide": [
                "pure_substance",
                "substance_identifiers",
                "elemental_composition",
                "sample_identifiers",
            ],
        },
    )

    case_id = Quantity(
        type=str,
        a_eln={
            "component": "StringEditQuantity",
            "label": "case-ID",
        },
    )

    CaseCrimpEnum = Enum(["manual", "hydraulic"])
    case_crimp = Quantity(
        type=CaseCrimpEnum, 
        a_eln={"component": "EnumEditQuantity", "label": "case-crimp"})

    pressure = Quantity(
        type=float,
        unit="pascal",
        a_eln={
            "component": "NumberEditQuantity", "label": "pressure (hydraulic only)",              
            "defaultDisplayUnit": "pascal",
        },
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if self.case_crimp == "manual":
            self.pressure = None


class BatteryCase(ArchiveSection):
    m_def = Section(label="Battery-Case",
                    a_eln=dict(overview=True)
    )
    
    case_id = Quantity(type=str, a_eln={"component": "StringEditQuantity", "label": "case-ID"})
    CaseCrimpEnum = Enum(["manual", "hydraulic"])
    case_crimp = Quantity(type=CaseCrimpEnum, a_eln={"component": "EnumEditQuantity", "label": "case-crimp"})
    pressure = Quantity(
        type=float, unit="pascal", 
        a_eln={
            "component": "NumberEditQuantity", "label": "pressure (hydraulic only)",              
            "defaultDisplayUnit": "pascal",
        },
    )

class CoinCellBattery2(BatterySample):
    m_def = Section(
        label="HZB Coin Cell Battery - 2",
        a_eln={
            "label": "HZB Coin Cell Battery - 2",
            "entry_type": "Coin Cell",
            "properties": {
                "order": [
                    "components",
                    "battery_case",
                ]
            },
             "hide": [
                "pure_substance",
                "substance_identifiers",
                "elemental_composition",
                "sample_identifiers",
            ],
        },
    )

    battery_case = SubSection(section_def=BatteryCase, repeats=False)

    def normalize(self, archive, logger):
        # create a section instance
        if self.battery_case is None:
            self.battery_case = BatteryCase() 

        if self.battery_case.case_crimp == "manual":
            self.battery_case.pressure = None

        super().normalize(archive, logger)


m_package.__init_metainfo__()
