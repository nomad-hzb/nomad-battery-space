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
    EntryData,
)
from nomad.datamodel.metainfo.basesections import (
    SectionReference,
)
from nomad.datamodel.metainfo.basesections.v1 import (
    ElementalComposition,
    EntityReference,
)
from nomad.datamodel.metainfo.eln import (
    ELNSubstance,
    Sample,
    SampleID,
)
from nomad.metainfo import (
    Quantity, 
    Reference, 
    SchemaPackage, 
    Section, 
    SubSection,
    Enum,
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
        a_eln={
            "label": "Anode",
            "entry_type": "Anode"
        }
    )
    
    mass = Quantity(
        type=float,
        description='Total mass of the anode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Mass (Anode)",
            "defaultDisplayUnit": "gram"
        },
        unit="gram",
    )

    area = Quantity(
        type=float,
        description='Geometric surface area of the anode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Area (Anode)",
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
        a_eln={
            "label": "Cathode",
            "entry_type": "Cathode"
        }
    )
    
    mass = Quantity(
        type=float,
        description='Total mass of the cathode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Mass (Cathode)",
            "defaultDisplayUnit": "gram"
        },
        unit="gram",
    )
    area = Quantity(
        type=float,
        description='Geometric surface area of the cathode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Area (Cathode)",
            "defaultDisplayUnit": "centimeter ** 2"
        },
        unit='centimeter ** 2',
    )
    mass_active_material = Quantity(
        type=float,
        description='Mass of the active material in the cathode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Mass of active material (Cathode)",
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
        a_eln={
            "properties": {
                "order": [
                    "state",                    
                    "volume",
                    "mass",
                ],
                "order_default": [
                    "description"
                ]
            },
            "label": "Electrolyte",
            "entry_type": "Electrolyte"
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
            "label": "Mass (Electrolyte)",
            "defaultDisplayUnit": "gram"
        },
        unit="gram",
    )
    volume = Quantity(
        type=float,
        description='Volume of the electrolyte.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Volume (Electrolyte)",
            "defaultDisplayUnit": "milliliter"
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
        a_eln={
            "properties": {
                "order": [
                    "composition",
                    "thickness"
                ]
            },
            "label": "Separator",
            "entry_type": "Separator"
        },
        )
    # composition = Quantity(
    #     type=str,
    #     description='Material composition of the separator (e.g., PP/PE).',
    #     a_eln={
    #         "component": "StringEditQuantity",
    #         "label": "Composition (Separator)"
    #     },
    # )
    thickness = Quantity(
        type=float,
        description='Thickness of the separator.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "Thickness (Separator)",
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
    # cathode = SubSection(
    #     section_def=Cathode,
    # )
    # electrolyte = SubSection(
    #     section_def=Electrolyte,
    # )
    # separator = SubSection(
    #     section_def=Separator,
    # )

class BatterySample(Sample, EntryData):
    '''
    Basic information about a battery sample including its components.
    '''
    m_def = Section(
        a_eln={
            "properties": {
                "order": [
                    "components",
                    "sample_identifiers"
                ]
            },
            "label": "Battery Sample",
            "entry_type": "Battery Sample"
        },
        label="Battery Sample",)
    components = SubSection(
        section_def=Components,
    )
    sample_identifiers = SubSection(
        section_def=SampleID,
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

m_package.__init_metainfo__()
