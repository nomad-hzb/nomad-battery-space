# Reference

## Entry types

| ELN label | Class (`m_def`) |
|---|---|
| HZB Battery: Chemical | `nomad_battery_space.schema_packages.hzb_bs_package.BS_Chemical` |
| HZB Battery: Electrode Material | `nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeMaterial` |
| HZB Battery: Electrode Sheet | `nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet` |
| HZB Battery: Electrolyte Stock | `nomad_battery_space.schema_packages.hzb_bs_package.ElectrolyteStock` |
| HZB Battery: Separator Stock | `nomad_battery_space.schema_packages.hzb_bs_package.SeparatorStock` |
| HZB Battery: Electrode Sample | `nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSample` |
| HZB Battery: Electrolyte Sample | `nomad_battery_space.schema_packages.hzb_bs_package.ElectrolyteSample` |
| HZB Battery: Separator Sample | `nomad_battery_space.schema_packages.hzb_bs_package.SeparatorSample` |
| HZB Battery: Generic Sample | `nomad_battery_space.schema_packages.hzb_bs_package.BatterySample` |
| HZB Battery: Coin Cell | `nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery` |
| HZB Battery: Measurement | `nomad_battery_space.schema_packages.hzb_bs_measurement_package.BS_Measurement` |

## Shared sections

These sections appear in several entry types.

### Dimensions and weights

Used by Electrode Sheet, Separator Stock, Electrode Sample and Separator Sample.

| Field | Unit | Description |
|---|---|---|
| **thickness** | µm | Thickness of the material. |
| **mass** | g | Mass of the material. |
| **shape** | | One of the [geometries](#geometry) below. |

### Volume and weights

Used by Electrode Material, Electrolyte Stock and Electrolyte Sample.

| Field | Unit | Description |
|---|---|---|
| **volume** | mL | Volume of the material or solution. |
| **mass** | g | Mass of the material or solution. |

### Geometry

The **shape** of a sample is one of:

| Shape | Class | Fields |
|---|---|---|
| **Circle** | `nomad_battery_space.schema_packages.utilities.geometry.CircleGeometry` | **diameter** (mm); **area** (cm²) is calculated. |
| **Rectangle** | `nomad_battery_space.schema_packages.utilities.geometry.RectangleGeometry` | **length** and **width** (mm); **area** (cm²) is calculated. |
| **Other** | `nomad_battery_space.schema_packages.utilities.geometry.OtherGeometry` | **shape description** (free text). |

### Product info

**product info / supplier**, for bought items. Available in every entry type except
Measurement.

| Field | Unit |
|---|---|
| **product number** | |
| **lot number** | |
| **product volume** | mL |
| **product weight** | g |
| **shipping date** | |
| **opening date** | |
| **supplier** | |
| **product description** | |
| **cost** | |

If the entry has a *volume and weights* or *dimensions and weights* section and its mass
or volume is empty, the product weight and product volume are copied there.

### Notes

A rich text field for anything that is not covered by the other fields. Available in
every entry type except Measurement.

## Schema packages

| Entry point | Content |
|---|---|
| `hzb_bs_package` | Chemical, stocks, samples and the generic battery sample. |
| `hzb_bs_assembly_package` | Specialized cell types (currently the coin cell). |
| `hzb_bs_measurement_package` | Measurement. |
| `hzb_utilities_processing` | Precursors and processing, shared by all stock types. |
| `hzb_utilities_dimensions` | Dimensions and weights, volume and weights. |
| `hzb_utilities_geometry` | Circle, rectangle and other geometry. |
| `hzb_utilities_notes` | Notes. |
| `hzb_utilities_voila_notebook` | Voila notebooks. |

## Apps

| App | Description |
|---|---|
| **HZB sample search app** | Search for battery entries, e.g. by entry type, lab ID or elements. |
| **Voila** | Find and launch Voila tools for battery space data. |
