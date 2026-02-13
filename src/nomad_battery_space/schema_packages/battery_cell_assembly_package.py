from nomad.metainfo import (
    Enum,
    Quantity,
    SchemaPackage,
    Section,
)

from .battery_sample_package import BatterySample
from .utils import validate_required

m_package = SchemaPackage()

# Shared configuration constant
DEFAULT_HIDE_FIELDS = [
    "pure_substance",
    "substance_identifiers",
    "elemental_composition",
    "sample_identifiers",
]


def create_millimeter_quantity(label, description, required=False):
    """Helper function to create millimeter-based float quantities."""
    return Quantity(
        type=float,
        unit="millimeter",
        description=description,
        a_eln={
            "component": "NumberEditQuantity",
            "label": label,
            "defaultDisplayUnit": "millimeter",
            "required": required,
        },
    )


def create_string_quantity(label, description=None, required=False):
    """Helper function to create string quantities."""
    return Quantity(
        type=str,
        description=description,
        a_eln={
            "component": "StringEditQuantity",
            "label": label,
            "required": required,
        },
    )

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
            "hide": DEFAULT_HIDE_FIELDS,
        },
    )

    case_id = create_string_quantity(
        "case-ID",
        description=(
            "Standardized coin cell housing code according to IEC 60086.\n\n"
            "Letters indicate the electrochemical system (e.g. CR = Li-MnO₂), "
            "followed by four digits: first two = nominal diameter (mm), "
            "last two = nominal height (0.1 mm).\n\n"
            "Example: CR2032 → 20 mm diameter, 3.2 mm height."
        ),
    )

    CaseCrimpEnum = Enum(["manual", "hydraulic"])
    case_crimp = Quantity(
        type=CaseCrimpEnum,
        description=None,
        a_eln={"component": "EnumEditQuantity", "label": "case-crimp"})

    pressure = Quantity(
        type=float,
        unit="MPa", # pascal
        description=None,
        a_eln={
            "component": "NumberEditQuantity", "label": "pressure (hydraulic only)",              
            "defaultDisplayUnit": "MPa",
        },
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if self.case_crimp == "manual":
            self.pressure = None


class PouchCellBattery(BatterySample):
    m_def = Section(
        links=['https://w3id.org/emmo/domain/battery#battery_392b3f47_d62a_4bd4_a819_b58b09b8843a'],
        label="HZB Pouch Cell Battery",
        a_eln={
            "label": "HZB Pouch Cell Battery",
            "entry_type": "Pouch Cell",
            "properties": {
                "order": [
                    "lab_id",
                    "name",
                    "datetime",
                    "cathode_length",
                    "cathode_width",
                    "number_of_layers",
                    "pouch_length",
                    "pouch_width",
                    "pouch_height",
                    "description",
                    "tags",
                    "components",
                ]
            },
            "hide": DEFAULT_HIDE_FIELDS,
        },
    )

    cathode_length = create_millimeter_quantity(
        label="cathode length", description="Cathode length", required=True
    )

    cathode_width = create_millimeter_quantity(
        label="cathode width", description="Cathode width", required=True
    )

    number_of_layers = Quantity(
        type=int,
        description="Number of layers",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "number of layers",
            "required": True,
        },
    )

    pouch_length = create_millimeter_quantity(
        label="pouch length", description="Pouch length"
    )

    pouch_width = create_millimeter_quantity(
        label="pouch width", description="Pouch width"
    )

    pouch_height = create_millimeter_quantity(
        label="pouch height", description="Pouch height"
    )

    def normalize(self, archive, logger):
        
        super().normalize(archive, logger)

        # validate mandatory fields 
        validate_required(self.cathode_length, name='cathode length')
        validate_required(self.cathode_width, name='cathode width')
        validate_required(self.number_of_layers, name='number of layers')


class CylindricalCellBattery(BatterySample):

    m_def = Section(
        links=[' https://w3id.org/emmo/domain/battery#battery_ac604ecd_cc60_4b98_b57c_74cd5d3ccd40'],
        label="HZB Cylindrical Cell Battery",
        a_eln={
            "label": "HZB Cylindrical Cell Battery",
            "entry_type": "Cylindrical Cell",
            "properties": {
                "order": [
                    "lab_id",
                    "name",
                    "datetime",
                    "description",
                    "cathode_length",
                    "cathode_width",
                    "case_id",
                    "cylindrical_length",
                    "cylindrical_diameter",
                    "tags",
                    "components",
                ]
            },
            "hide": DEFAULT_HIDE_FIELDS,
        },
    )

    cathode_length = create_millimeter_quantity(label="cathode length", description="Cathode length")

    cathode_width = create_millimeter_quantity(label="cathode width", description="Cathode width")

    case_id = create_string_quantity(
        "case-ID",
        description=(
            "Standardized cylindrical cell housing code according to IEC 60086.\n\n"
            "For cylindrical cells, the designation typically consists of letters indicating "
            "the electrochemical system (e.g. LR = alkaline, CR = lithium manganese dioxide) "
            "followed by digits defining the standardized size.\n\n"
            "For numeric codes (e.g. 18650), the first two digits indicate the nominal diameter (mm), "
            "the next two or three digits the nominal height (mm), and a trailing '0' indicates cylindrical shape.\n\n"
            "Example: 18650 → 18 mm diameter, 65 mm height, cylindrical form."
        ),
    )

    cylindrical_length = create_millimeter_quantity(label="cylindrical length", description="Cylindrical length")

    cylindrical_diameter = create_millimeter_quantity(label="cylindrical diameter", description="Cylindrical diameter")

    def normalize(self, archive, logger):
        
        super().normalize(archive, logger)

        # validate mandatory fields 
        validate_required(self.cathode_length, name='cathode length')
        validate_required(self.cathode_width, name='cathode width')
        


m_package.__init_metainfo__()

# class BatteryCase(ArchiveSection):
#     m_def = Section(label="Battery-Case",
#                     a_eln=dict(overview=True)
#     )
    
#     case_id = Quantity(type=str, a_eln={"component": "StringEditQuantity", "label": "case-ID"})
#     CaseCrimpEnum = Enum(["manual", "hydraulic"])
#     case_crimp = Quantity(type=CaseCrimpEnum, a_eln={"component": "EnumEditQuantity", "label": "case-crimp"})
#     pressure = Quantity(
#         type=float, unit="pascal", 
#         a_eln={
#             "component": "NumberEditQuantity", "label": "pressure (hydraulic only)",              
#             "defaultDisplayUnit": "pascal",
#         },
#     )

# class CoinCellBattery2(BatterySample):
#     m_def = Section(
#         label="HZB Coin Cell Battery - 2",
#         a_eln={
#             "label": "HZB Coin Cell Battery - 2",
#             "entry_type": "Coin Cell",
#             "properties": {
#                 "order": [
#                     "components",
#                     "battery_case",
#                 ]
#             },
#              "hide": [
#                 "pure_substance",
#                 "substance_identifiers",
#                 "elemental_composition",
#                 "sample_identifiers",
#             ],
#         },
#     )

#     battery_case = SubSection(section_def=BatteryCase, repeats=False)

#     def normalize(self, archive, logger):
#         # create a section instance
#         if self.battery_case is None:
#             self.battery_case = BatteryCase() 

#         if self.battery_case.case_crimp == "manual":
#             self.battery_case.pressure = None

#         super().normalize(archive, logger)




# class BatteryCellAssemblyBase(ArchiveSection):
#     m_def = Section(a_eln={"overview": True})

#     cell_id = Quantity(type=str, a_eln={"component": "StringEditQuantity"})

#     stack_order = Quantity(
#         type=MEnum(
#             "Cathode → Anode",
#             "Anode → Cathode",
#         ),
#         description="Order in which the electrodes are stacked during cell assembly.",
#         a_eln={
#             "component": "EnumEditQuantity"
#         },
#     )

#     procedure = Quantity(type=str, a_eln={"component": "RichTextEditQuantity", "props": {"height": 100}})
#     procedure_sketch = Quantity(type=str, a_eln={"component": "FileEditQuantity"})  # photo/PDF


# class CoinCellAssembly(BatteryCellAssemblyBase):
#     m_def = Section(a_eln={"properties": {"order": ["cell_id", "stack_order", "crimping_pressure", "procedure", "procedure_sketch"]}})

#     crimping_pressure = Quantity(type=float, unit="MPa", a_eln={"component": "NumberEditQuantity"})
#     crimper_model = Quantity(type=str, a_eln={"component": "StringEditQuantity"})
#     spacer_thickness = Quantity(type=float, unit="mm", a_eln={"component": "NumberEditQuantity"})

# class OperandoCellAssembly(BatteryCellAssemblyBase):
#     window_material = Quantity(type=str, a_eln={"component": "StringEditQuantity"})
#     leak_test = Quantity(type=str, a_eln={"component": "RichTextEditQuantity"})

# class PouchCellAssembly(BatteryCellAssemblyBase):
#     pouch_film = Quantity(type=str, a_eln={"component": "StringEditQuantity"})
#     sealing_temperature = Quantity(type=float, unit="degC", a_eln={"component": "NumberEditQuantity"})
#     sealing_time = Quantity(type=float, unit="s", a_eln={"component": "NumberEditQuantity"})

