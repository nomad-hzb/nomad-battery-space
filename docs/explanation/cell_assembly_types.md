# Battery Cell Assembly Types

This document describes the three specialized battery cell types available in the `nomad-battery-space` plugin. Each type extends the base `BatterySample` class with geometry and specification fields specific to that cell form factor.

## Overview

All battery cell types share common base properties from `BatterySample`:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| **battery name** | string | Yes | Descriptive name of the battery entry |
| **lab_id** | string | Yes | Lab-specific identifier (must be unique within lab) |
| **description** | string | No | Detailed description of the battery |
| **datetime** | datetime | No | Creation/assembly date and time |
| **components** | section | No | References to Anode, Cathode, Electrolyte, and Separator |
| **aggregated elements** | section | No | Aggregated elementary and compound components |

All specialized types inherit these properties and add type-specific fields for geometry and assembly parameters.

---

## Coin Cell Battery

For coin-shaped battery cells following IEC 60086 standardization.

### Entry Type: `CoinCellBattery`

### Specific Properties

| Property | Type | Unit | Required | Description |
|----------|------|------|----------|-------------|
| **case_id** | string | — | No | IEC 60086 code (e.g., "CR2032", "CR2025") |
| **case_crimp** | enum | — | No | Assembly method: "manual" or "hydraulic" |
| **pressure** | float | MPa | No | Crimping pressure (hydraulic only) |

### Example Data

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery
  lab_id: CC_001
  name: coin_cell_cr2032_01
  datetime: 2024-01-15T10:30:00Z
  description: Test coin cell for electrochemical performance evaluation
  case_id: CR2032
  case_crimp: manual
  components:
    anode_q: '#anode_01'
    cathode_q: '#cathode_01'
    electrolyte_q: '#electrolyte_01'
    separator_q: '#separator_01'
  sample_identifiers:
    sample_id: CC_ABC123
```

---

## Pouch Cell Battery

For single-unit flexible packet battery cells.

### Entry Type: `PouchCellBattery`

### Specific Properties

| Property | Type | Unit | Required | Description |
|----------|------|------|----------|-------------|
| **cathode_length** | float | mm | Yes | Length of cathode electrode |
| **cathode_width** | float | mm | Yes | Width of cathode electrode |
| **number_of_layers** | int | — | Yes | Number of anode-cathode layer pairs (stack count) |
| **pouch_length** | float | mm | No | External length of pouch envelope |
| **pouch_width** | float | mm | No | External width of pouch envelope |
| **pouch_height** | float | mm | No | Thickness of pouch package |

### Example Data

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_assembly_package.PouchCellBattery
  lab_id: PC_001
  name: pouch_cell_01
  datetime: 2024-02-10T14:45:00Z
  description: Multi-layer pouch cell for high-capacity testing
  cathode_length: 50.5
  cathode_width: 40.0
  number_of_layers: 3
  pouch_length: 60.0
  pouch_width: 50.0
  pouch_height: 5.5
  components:
    anode_q: '#anode_01'
    cathode_q: '#cathode_01'
    electrolyte_q: '#electrolyte_01'
    separator_q: '#separator_01'
  sample_identifiers:
    sample_id: PC_DEF456
```

---

## Cylindrical Cell Battery

For cylindrical form factor battery cells (18650, 21700, 32650, etc.).

### Entry Type: `CylindricalCellBattery`

### Specific Properties

| Property | Type | Unit | Required | Description |
|----------|------|------|----------|-------------|
| **case_id** | string | — | No | Standardized cylindrical cell code (e.g., "18650", "21700") |
| **cathode_length** | float | mm | No | Length of cathode electrode |
| **cathode_width** | float | mm | No | Width of cathode electrode |
| **cylindrical_length** | float | mm | No | Total length of cylindrical cell |
| **cylindrical_diameter** | float | mm | No | Outer diameter of cylindrical cell |

### Example Data

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_assembly_package.CylindricalCellBattery
  lab_id: CYL_001
  name: cylindrical_cell_18650_01
  datetime: 2024-03-05T09:20:00Z
  description: Cylindrical cell for high-energy-density application
  case_id: '18650'
  cathode_length: 45.0
  cathode_width: 42.0
  cylindrical_length: 65.0
  cylindrical_diameter: 18.0
  components:
    anode_q: '#anode_01'
    cathode_q: '#cathode_01'
    electrolyte_q: '#electrolyte_01'
    separator_q: '#separator_01'
```

---

## Related Documentation

- See [Component Types](component_types.md) for properties of referenced components
- See [Reference Model](reference_model.md) for the reference system
- See [Tutorial](../tutorial/tutorial.md) for step-by-step assembly examples
