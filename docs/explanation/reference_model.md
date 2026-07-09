# Battery Data Schema – Reference Model

## Overview

The `nomad-battery-space` plugin implements a modular schema for documenting battery systems. The design philosophy separates concerns by defining battery components as independent entries that are then referenced by battery samples.

This approach offers several advantages:

- **Reusability**: A single Anode entry can be referenced by multiple battery samples
- **Data integrity**: Component properties are stored once and updated in one place
- **Workflow efficiency**: Components can be created independently and reused across experiments
- **Traceability**: Reference quantities maintain explicit links between batteries and their components

## Component Types

The plugin defines four core battery component types as independent ELN entries:

| Component | Key Properties | Purpose |
|-----------|----------------|---------|
| **Anode** | mass, geometric area | Negative electrode material documentation |
| **Cathode** | mass, geometric area, active material mass | Positive electrode material documentation |
| **Electrolyte** | mass, volume, physical state (Liquid/Solid) | Electrolyte composition and quantity documentation |
| **Separator** | thickness | Separator material specification |

All components inherit from `ELNSubstance` (from NOMAD's data model), which provides standard substance properties like name, description, and material composition.

## Battery Sample Architecture

### Reference-based Component Model

Battery samples do not embed components directly. Instead, they use **reference quantities** to link to component entries:

```python
class Components(ArchiveSection):
    '''Pure UI grouping container inside BatterySample.'''
    anode_q = Quantity(type=Reference(Anode.m_def))
    cathode_q = Quantity(type=Reference(Cathode.m_def))
    electrolyte_q = Quantity(type=Reference(Electrolyte.m_def))
    separator_q = Quantity(type=Reference(Separator.m_def))
```

This design allows the `BatterySample` class to be extended by specialized cell types (see [Cell Assembly Types](cell_assembly_types.md)) without duplicating component handling logic.

### Creating a Battery Sample

The typical workflow is:

1. Create component entries independently

   - Anode entry with mass and area measurements
   - Cathode entry with mass and active material specification
   - Electrolyte entry with mass, volume, and state
   - Separator entry with thickness measurement

2. Create BatterySample and reference components
   ```yaml
   data:
     m_def: nomad_battery_space.schema_packages.hzb_bs_package.BatterySample
     name: battery_sample_01
     lab_id: BAT_001
     components:
       anode_q: '#anode_01'
       cathode_q: '#cathode_01'
       electrolyte_q: '#electrolyte_01'
       separator_q: '#separator_01'
   ```

### Normalization Behavior

During the normalization phase:

- Component references are validated but not dereferenced (dereferencing occurs during server-side processing)
- Elemental composition is aggregated from referenced components into `aggregated_elements`
- Material results are populated in the archive's results section for search and discovery

All reference values remain unchanged; the references themselves are not modified during normalization.

## Extended Battery Cell Types

The plugin provides three specialized battery cell sub-types that extend `BatterySample`:

- **CoinCellBattery**: Adds coin cell specifications (case ID, crimp method, pressure)
- **PouchCellBattery**: Adds pouch cell geometry (cathode dimensions, number of layers, pouch envelope)
- **CylindricalCellBattery**: Adds cylindrical cell specs (case ID, cylindrical dimensions)

See [Cell Assembly Types](cell_assembly_types.md) for detailed specifications of each type.

## Data Model Example

```
User Creates:
├── Anode [anode_01]
├── Cathode [cathode_01]
├── Electrolyte [electrolyte_01]
├── Separator [separator_01]
└── BatterySample [battery_sample_01]
     └── Components (grouping section)
         ├── anode_q → Reference to anode_01
         ├── cathode_q → Reference to cathode_01
         ├── electrolyte_q → Reference to electrolyte_01
         └── separator_q → Reference to separator_01
```

## Testing Strategy

Because plugin tests run without the NOMAD processing backend:

- Full reference dereferencing is not supported during testing
- You can validate the structure and presence of references
- You can check reference values (the reference strings themselves)
- You can verify component metadata after normalization

Tests focus on:

- Reference quantity presence and correct types
- Metadata validation (e.g. name, lab_id)
- Correct normalization of aggregated fields
- Enforced required field validation

See test files for complete examples of the testing approach.