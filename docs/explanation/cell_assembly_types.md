# Battery Cells

A battery cell entry combines the samples that were assembled into one cell: electrodes,
separator and electrolyte.

There are two kinds of cell entries:

- the generic [Battery Sample](#battery-sample), which works for every cell format, and
- [specialized cell types](#specialized-cell-types) for specific formats. They have all
  fields of the battery sample plus fields for their format.

## Battery Sample

**ELN label:** HZB Battery: Generic Sample · **Class:** `BatterySample`

The generic cell entry, used for any cell format. It is also the base of all
[specialized cell types](#specialized-cell-types). Use it for formats that have no
specialized type yet.

| Field | Required | Description |
|---|---|---|
| **battery ID** (`lab_id`) | Yes | Human-readable ID of the cell, unique at least within the lab. |
| **battery name** (`name`) | Yes | Name of the entry. |
| **datetime** | | Date and time of assembly. |
| **working electrode** | | The [Electrode Sample](component_types.md#electrode-sample) used as working electrode. |
| **counter electrode** | | The [Electrode Sample](component_types.md#electrode-sample) used as counter electrode. |
| **reference electrode** | | Optional, for three-electrode setups. |
| **separator** | | The [Separator Sample](component_types.md#separator-sample). |
| **electrolyte** | | The [Electrolyte Sample](component_types.md#electrolyte-sample). |
| **procedure sketch** | | Photo or PDF of the assembly procedure or a technical drawing. |
| **aggregated elements** | | Filled automatically from all components, see [Aggregated elements](reference_model.md#aggregated-elements). |
| **product info / supplier** | | For bought cells. |
| **sample identifiers** | | Further identifiers (collapsed by default). |
| **notes** | | Free text. |

Electrodes are named by their function in the measurement (working, counter, reference),
not by their polarity: whether the working electrode is the anode or the cathode depends
on the setup.

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_package.BatterySample
  lab_id: BAT_001
  name: half_cell_NMC111_01
  datetime: 2026-01-15T10:30:00Z
  working_electrode: '../upload/archive/mainfile/NMC111_sheet_01_disc_03.archive.yaml#data'
  counter_electrode: '../upload/archive/mainfile/Li_foil_disc_01.archive.yaml#data'
  separator: '../upload/archive/mainfile/Celgard_2400_disc_01.archive.yaml#data'
  electrolyte: '../upload/archive/mainfile/LP30_cell_01.archive.yaml#data'
```

---

## Specialized cell types

A specialized cell type extends the [Battery Sample](#battery-sample) with fields for
one cell format, e.g. the case or the crimping of a coin cell. Electrodes, separator,
electrolyte and the aggregation of elements work the same for all of them.

Currently available:

| Cell type | ELN label | Class |
|---|---|---|
| [Coin Cell](#coin-cell) | HZB Battery: Coin Cell | `CoinCellBattery` |

More cell types will be added.

### Coin Cell

**ELN label:** HZB Battery: Coin Cell · **Class:** `CoinCellBattery`

A coin cell. It has all fields of the [Battery Sample](#battery-sample) plus:

| Field | Unit | Description |
|---|---|---|
| **case-id** | | Case code: the first two digits are the diameter in mm, the last two the height in 0.1 mm. Suggestions: `2032` (20 mm × 3.2 mm), `2025` (20 mm × 2.5 mm), `operando` (self-built cells for in-situ measurements). Other values are allowed. |
| **case-crimp** | | `manual` (default) or `automatic`. |
| **pressure** | MPa | Crimping pressure. Only used for automatic crimping; for manual crimping it is cleared on save. |

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery
  lab_id: CC_001
  name: coin_cell_01
  datetime: 2026-01-15T10:30:00Z
  case_id: '2032'
  case_crimp: automatic
  pressure: 0.8
  working_electrode: '../upload/archive/mainfile/NMC111_sheet_01_disc_03.archive.yaml#data'
  counter_electrode: '../upload/archive/mainfile/Li_foil_disc_01.archive.yaml#data'
  separator: '../upload/archive/mainfile/Celgard_2400_disc_01.archive.yaml#data'
  electrolyte: '../upload/archive/mainfile/LP30_cell_01.archive.yaml#data'
```

## Related pages

- [Materials and Components](component_types.md): the samples referenced by a cell.
- [Measurements](measurements.md): attaching measurement data to a cell.
