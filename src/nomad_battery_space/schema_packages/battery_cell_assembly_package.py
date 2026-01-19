from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import MEnum, Quantity, Section


class BatteryCellAssemblyBase(ArchiveSection):
    m_def = Section(a_eln={"overview": True})

    cell_id = Quantity(type=str, a_eln={"component": "StringEditQuantity"})

    stack_order = Quantity(
        type=MEnum(
            "Cathode → Anode",
            "Anode → Cathode",
        ),
        description="Order in which the electrodes are stacked during cell assembly.",
        a_eln={
            "component": "EnumEditQuantity"
        },
    )

    procedure = Quantity(type=str, a_eln={"component": "RichTextEditQuantity", "props": {"height": 100}})
    procedure_sketch = Quantity(type=str, a_eln={"component": "FileEditQuantity"})  # photo/PDF


class CoinCellAssembly(BatteryCellAssemblyBase):
    m_def = Section(a_eln={"properties": {"order": ["cell_id", "stack_order", "crimping_pressure", "procedure", "procedure_sketch"]}})

    crimping_pressure = Quantity(type=float, unit="MPa", a_eln={"component": "NumberEditQuantity"})
    crimper_model = Quantity(type=str, a_eln={"component": "StringEditQuantity"})
    spacer_thickness = Quantity(type=float, unit="mm", a_eln={"component": "NumberEditQuantity"})

class OperandoCellAssembly(BatteryCellAssemblyBase):
    window_material = Quantity(type=str, a_eln={"component": "StringEditQuantity"})
    leak_test = Quantity(type=str, a_eln={"component": "RichTextEditQuantity"})

class PouchCellAssembly(BatteryCellAssemblyBase):
    pouch_film = Quantity(type=str, a_eln={"component": "StringEditQuantity"})
    sealing_temperature = Quantity(type=float, unit="degC", a_eln={"component": "NumberEditQuantity"})
    sealing_time = Quantity(type=float, unit="s", a_eln={"component": "NumberEditQuantity"})

