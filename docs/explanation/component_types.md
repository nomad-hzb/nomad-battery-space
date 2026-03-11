# Battery Component Types

This document provides detailed specifications for each battery component type in the `nomad-battery-space` plugin.

## Overview

Battery components are standalone ELN entries that can be created independent of any battery sample. Each component type extends NOMAD's `ELNSubstance` class, inheriting standard substance properties and adding battery-specific measurements.

All components support:

- **name**: Entry identifier (e.g., "anode_01")
- **description**: Detailed documentation
- **elemental_composition**: Material composition (inherited from ELNSubstance)


## Anode

The negative electrode component in a battery cell.

### Properties

| Property | Type | Unit | Required | Description |
|----------|------|------|----------|-------------|
| **name** | string | — | Yes | Unique identifier for the anode |
| **mass** | float | g | No | Total mass of the anode material |
| **area** | float | cm² | No | Geometric surface area of the anode |
| **description** | string | — | No | Detailed information about the anode |
| **elemental_composition** | list | — | No | Elemental composition data |

### Example Data

```yaml
data:
  m_def: nomad_battery_space.schema_packages.battery_sample_package.Anode
  name: Lithium
  mass: 0.008
  area: 1.54
  description: "Lithium metal anode prepared by electrochemical deposition"
  elemental_composition:
    - element: Li
```

---

## Cathode

The positive electrode component in a battery cell.

### Properties

| Property | Type | Unit | Required | Description |
|----------|------|------|----------|-------------|
| **name** | string | — | Yes | Unique identifier for the cathode |
| **mass** | float | g | No | Total mass of the cathode material |
| **area** | float | cm² | No | Geometric surface area of the cathode |
| **mass_active_material** | float | % | No | Mass percentage of active material in the cathode |
| **description** | string | — | No | Detailed information about the cathode |
| **elemental_composition** | list | — | No | Elemental composition data |

### Example Data

```yaml
data:
  m_def: nomad_battery_space.schema_packages.battery_sample_package.Cathode
  name: Copper
  mass: 0.14
  area: 1.54
  mass_active_material: 100
  description: "Copper cathode prepared by electrochemical deposition"
  elemental_composition:
    - element: Cu
```

---

## Electrolyte

The ionic conductor component that enables charge transport between anode and cathode.

### Properties

| Property | Type | Unit | Required | Description |
|----------|------|------|----------|-------------|
| **name** | string | — | Yes | Unique identifier for the electrolyte |
| **state** | enum | — | Yes | Physical state: "Liquid" or "Solid" |
| **mass** | float | g | No | Total mass of the electrolyte |
| **volume** | float | mL | No | Volume of the electrolyte |
| **description** | string | — | No | Detailed information about the electrolyte |
| **elemental_composition** | list | — | No | Elemental composition data |

### Example Data

```yaml
data:
  m_def: nomad_battery_space.schema_packages.battery_sample_package.Electrolyte
  name: Sulphuric acid
  state: Liquid
  mass: 0.108
  volume: 0.1
  description: "Sulfuric acid (H₂SO₄) electrolyte solution"
  elemental_composition:
    - element: H
    - element: S
    - element: O
```

---

## Separator

The physical barrier that prevents electrode contact while allowing ionic transport.

### Properties

| Property | Type | Unit | Required | Description |
|----------|------|------|----------|-------------|
| **name** | string | — | Yes | Unique identifier for the separator |
| **thickness** | float | μm | No | Thickness of the separator material |
| **description** | string | — | No | Detailed information about the separator |
| **elemental_composition** | list | — | No | Elemental composition data (if applicable) |

### Example Data

```yaml
data:
  m_def: nomad_battery_space.schema_packages.battery_sample_package.Separator
  name: Polypropylene
  thickness: 50.0
  description: "Polypropylene (C₃H₆)ₙ microporous separator with thermal shutdown capability"
  elemental_composition:
    - element: C
    - element: H
```

---

## Related Documentation

- See [Battery Sample Model](reference_model.md) for how components are referenced
- See [Cell Assembly Types](cell_assembly_types.md) for battery-level properties
- See [Tutorial](../tutorial/tutorial.md) for step-by-step examples
