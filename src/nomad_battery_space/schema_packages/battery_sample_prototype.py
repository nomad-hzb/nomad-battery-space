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

from nomad.datamodel.data import (
    ArchiveSection,
)
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

m_package = SchemaPackage()


class Anode(ELNSubstance):
    '''
    An anode entry in the battery schema.
    '''    
    m_def = Section(
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
    # elemental_composition = SubSection(
    #     section_def=ElementalComposition,
    #     repeats=True,
    # )

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

    VolumeUnitEnum = Enum(['l', 'ml', 'ul'])
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
    volume_value = Quantity(
        type=float,
        description="Volume of the electrolyte (value only, unit chosen separately).",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Volume",
        },
    )

    volume_unit = Quantity(
        type=VolumeUnitEnum,
        description="Volume unit",
        a_eln={
            "component": "EnumEditQuantity",
            "label": "Unit",
        },
        default="ml",
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
        type=Reference(Anode.m_def),
        description='Reference to an Anode entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Anode"
        },
    )
    # anode_subsection = SubSection(
    #     section_def=AnodeReference,
    #     description="""
    #     The anode as a composite part of the battery.
    #     """,
    # )
    cathode_q = Quantity(
        type=Reference(Cathode.m_def),
        description='Reference to a Cathode entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Cathode"
        },
    )
    electrolyte_q = Quantity(
        type=Reference(Electrolyte.m_def),
        description='Reference to a Electrolyte entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Electrolyte"
        },
    )
    separator_q = Quantity(
        type=Reference(Separator.m_def),
        description='Reference to a Separator entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Separator"
        },
    )
    
#class BatterySample(Sample, EntryData):
class BatterySample(ELNSubstance):
    '''
    Basic information about a battery sample including its components.
    '''
    #m_section_label = 'HZB Battery Space'
    m_def = Section(
        label="HZB Battery Sample",
        a_eln={
            "properties": {
                "order": [
                    "components",
                    "sample_identifiers"
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
            # RO, only for controlling purpuses => remove later?
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
        
m_package.__init_metainfo__()
