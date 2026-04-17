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
    AuthorReference,
    EntryData,
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

from .utils import create_area_quantity, create_string_quantity, validate_required
from baseclasses.voila import VoilaNotebook

m_package = SchemaPackage()


class CreatorReference(AuthorReference):
    """
    Custom AuthorReference that serializes User/Author objects as dicts for proper GUI display.
    
    The standard AuthorReference._serialize_impl() returns just the user_id string,
    which causes the AuthorEditQuantity GUI component to show empty because it expects
    a dict with a user_id property.
    
    This custom type serializes User/Author objects as dicts: {"user_id": "...", "name": "..."}
    while still properly deserializing string user_ids back to User objects.
    """
    
    def _serialize_impl(self, section, value):
        """Serialize User/Author objects as dicts instead of just strings"""
        if isinstance(value, str):
            # Keep strings as-is (they'll be converted back in _normalize_impl)
            return value
        
        if isinstance(value, dict):
            # Already a dict, return as-is
            return value
        
        # Handle Author and User objects (which don't have m_to_dict or have special handling)
        if hasattr(value, 'user_id') or hasattr(value, 'first_name'):
            # User object or Author object - serialize to dict
            result = {}
            if hasattr(value, 'user_id'):
                result['user_id'] = value.user_id
            if hasattr(value, 'name'):
                result['name'] = value.name
            if hasattr(value, 'first_name'):
                result['first_name'] = value.first_name
            if hasattr(value, 'last_name'):
                result['last_name'] = value.last_name
            if hasattr(value, 'email'):
                result['email'] = value.email
            if hasattr(value, 'affiliation'):
                result['affiliation'] = value.affiliation
            if hasattr(value, 'affiliation_address'):
                result['affiliation_address'] = value.affiliation_address
            return result
        
        # Fallback: try to convert to dict using m_to_dict if available
        if hasattr(value, 'm_to_dict'):
            try:
                return value.m_to_dict()
            except Exception:
                pass
        
        raise ValueError(f'Cannot serialize {value}.')


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
                    "creator", 
                    "mass",
                    "area",
                    "supplier",
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
            "label": "mass",
            "defaultDisplayUnit": "gram"
        },
        unit="gram",
    )

    area = create_area_quantity(
        label="area",
        description='Geometric surface area of the anode.',
    )

    supplier = create_string_quantity(
        "supplier",
        description=(
            "Manufacturer or seller of the material.\n"
            "Include company name and/or product designation (e.g., MTI).\n"
            "Essential for material sourcing and reproducibility."
        ),
    )

    creator = Quantity(
        type=CreatorReference,
        description='Person who created this anode entry.',
        a_eln={
            "component": "AuthorEditQuantity",
            "label": "creator",
        },
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
        
        # Auto-fill creator field with current user if empty
        if not self.creator and archive.metadata.main_author:
            from nomad.datamodel.data import User
            main_author = archive.metadata.main_author
            
            # Handle both cases: main_author can be a User object or a string user_id
            if isinstance(main_author, User):
                # Already a User object, just assign it
                self.creator = main_author
            else:
                # It's a string user_id, need to fetch the User object
                try:
                    user = User.get(user_id=main_author)
                    if user:
                        self.creator = user
                    else:
                        self.creator = main_author
                except Exception as e:
                    logger.warning(f"Could not fetch User for creator: {e}")
                    self.creator = main_author

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
                    "creator", 
                    "mass",
                    "area",
                    "mass_active_material",
                    "supplier",
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
            "label": "mass",
            "defaultDisplayUnit": "gram"
        },
        unit="gram",
    )
    area = create_area_quantity(
        label="area",
        description='Geometric surface area of the cathode.',
    )
    mass_active_material = Quantity(
        type=float,
        description='Mass of the active material in the cathode.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "mass of active material",
            "defaultDisplayUnit": "%"
        },
        unit="dimensionless",
    )

    supplier = create_string_quantity(
        "supplier",
        description=(
            "Manufacturer or seller of the material.\n "
            "Include company name and/or product designation (e.g., MTI).\n\n"
            "Essential for material sourcing and reproducibility."
        ),
    )

    creator = Quantity(
        type=CreatorReference,
        description='Person who created this cathode entry.',
        a_eln={
            "component": "AuthorEditQuantity",
            "label": "creator",
        },
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
        
        # Auto-fill creator field with current user if empty
        if not self.creator and archive.metadata.main_author:
            from nomad.datamodel.data import User
            main_author = archive.metadata.main_author
            
            # Handle both cases: main_author can be a User object or a string user_id
            if isinstance(main_author, User):
                # Already a User object, just assign it
                self.creator = main_author
            else:
                # It's a string user_id, need to fetch the User object
                try:
                    user = User.get(user_id=main_author)
                    if user:
                        self.creator = user
                    else:
                        self.creator = main_author
                except Exception as e:
                    logger.warning(f"Could not fetch User for creator: {e}")
                    self.creator = main_author


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
                    "creator",                   
                    "volume",
                    "mass",
                    "supplier",
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
            "label": "state",
        }
    )
    mass = Quantity(
        type=float,
        description='Total mass of the electrolyte.',
        a_eln={
            "component": "NumberEditQuantity",
            "label": "mass",
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
            "label": "volume",
            "defaultDisplayUnit": "milliliter",
            "units": ["liter", "milliliter", "microliter"],
        },
        unit="milliliter",
    )

    supplier = create_string_quantity(
        "supplier",
        description=(
            "Manufacturer or seller of the material.\n"
            "Include company name and/or product designation (e.g., MTI).\n"
            "Essential for material sourcing and reproducibility."
        ),
    )

    creator = Quantity(
        type=CreatorReference,
        description='Person who created this electrolyte entry.',
        a_eln={
            "component": "AuthorEditQuantity",
            "label": "creator",
        },
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
        
        # Auto-fill creator field with current user if empty
        if not self.creator and archive.metadata.main_author:
            from nomad.datamodel.data import User
            main_author = archive.metadata.main_author
            
            # Handle both cases: main_author can be a User object or a string user_id
            if isinstance(main_author, User):
                # Already a User object, just assign it
                self.creator = main_author
            else:
                # It's a string user_id, need to fetch the User object
                try:
                    user = User.get(user_id=main_author)
                    if user:
                        self.creator = user
                    else:
                        self.creator = main_author
                except Exception as e:
                    logger.warning(f"Could not fetch User for creator: {e}")
                    self.creator = main_author


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
                    "creator",
                    "thickness",
                    "area",
                    "supplier",
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

    area = create_area_quantity(
        label="area",
        description='Geometric surface area of the separator.',
    )

    supplier = create_string_quantity(
        "supplier",
        description=(
            "Manufacturer or seller of the material.\n"
            "Include company name and/or product designation (e.g., MTI).\n"
            "Essential for material sourcing and reproducibility."
        ),
    )

    creator = Quantity(
        type=CreatorReference,
        description='Person who created this separator entry.',
        a_eln={
            "component": "AuthorEditQuantity",
            "label": "creator",
        },
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
        
        # Auto-fill creator field with current user if empty
        if not self.creator and archive.metadata.main_author:
            from nomad.datamodel.data import User
            main_author = archive.metadata.main_author
            
            # Handle both cases: main_author can be a User object or a string user_id
            if isinstance(main_author, User):
                # Already a User object, just assign it
                self.creator = main_author
            else:
                # It's a string user_id, need to fetch the User object
                try:
                    user = User.get(user_id=main_author)
                    if user:
                        self.creator = user
                    else:
                        self.creator = main_author
                except Exception as e:
                    logger.warning(f"Could not fetch User for creator: {e}")
                    self.creator = main_author


# class AnodeReference(EntityReference):
#     """
#     A section used for referencing an Anode into a Battery.
#     """

#     reference = Quantity(
#         type=Anode,
#         description='A reference to a Battery `Anode` entry.',
#         a_eln={
#             "component": 'ReferenceEditQuantity',
#             "label": 'Anode',
#         },
#     )


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
            "label": "Anode",
            "showSectionLabel": True
        },
    )
    cathode_q = Quantity(
        type=Reference(Cathode.m_def),
        description='Reference to a Cathode entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Cathode",
            "showSectionLabel": True
        },
    )
    electrolyte_q = Quantity(
        type=Reference(Electrolyte.m_def),
        description='Reference to a Electrolyte entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Electrolyte",
            "showSectionLabel": True
        },
    )
    separator_q = Quantity(
        type=Reference(Separator.m_def),
        description='Reference to a Separator entry.',
        a_eln={
            "component": "ReferenceEditQuantity",
            "label": "Separator",
            "showSectionLabel": True
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
                    "creator",
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

    creator = Quantity(
        type=CreatorReference,
        description='Person who created this battery entry.',
        a_eln={
            "component": "AuthorEditQuantity",
            "label": "creator",
        },
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
        
        # Auto-fill creator field with current user if empty
        if not self.creator and archive.metadata.main_author:
            try:
                from nomad.datamodel.data import User
                # Fetch the full User object to ensure GUI can display it
                user = User.get(user_id=archive.metadata.main_author)
                if user:
                    self.creator = user
                else:
                    self.creator = archive.metadata.main_author
            except Exception as e:
                logger.warning(f"Could not fetch User for creator: {e}")
                self.creator = archive.metadata.main_author

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
        

class BatSpace_VoilaNotebook(VoilaNotebook, EntryData):
    m_def = Section(a_eln=dict(hide=['lab_id']))

    def normalize(self, archive, logger):
        super().normalize(archive, logger)


m_package.__init_metainfo__()
