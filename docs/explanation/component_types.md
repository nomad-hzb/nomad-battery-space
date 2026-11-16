# Materials and Components

This page describes all entry types below the cell level: the chemical, the four stock
types and the three sample types. For how they are connected, see
[Links between entries](reference_model.md).

All of these entry types are based on NOMAD's `ELNSubstance`. They share:

- **name**: the name of the entry.
- **lab ID**: a human-readable ID. Other entries can reference this entry by its lab ID.
- **substance identifiers**: further identifiers (collapsed by default).
- **notes**: a free text field for anything not covered by the other fields, see [Notes](../reference/references.md#notes).

All except the chemical also have **aggregated elements**, which are filled automatically,
see [Aggregated elements](reference_model.md#aggregated-elements).

Stocks and the chemical additionally have **elemental composition** and **pure substance**
from `ELNSubstance`. For samples these fields are hidden, because their composition comes
from the stock they were cut from.

The fields `chemicals`, `product info`, `dimensions and weights` and `volume and weights`
appear in several entry types. They are described once in the
[Reference](../reference/references.md).

---

## Chemical

**ELN label:** HZB Battery: Chemical · **Class:** `BS_Chemical`

A substance purchased from a supplier. Chemicals are the starting material for electrode
materials, electrode sheets, electrolyte stocks and separator stocks.

| Field | Description |
|---|---|
| **name** | Name of the chemical. |
| **elemental composition** | Elements of the chemical. They are passed on to every entry that uses this chemical. |
| **pure substance** | Optional PubChem-based substance information. |
| **product info / supplier** | Supplier, product and lot number, see [Product info](../reference/references.md#product-info). |

---

## Electrode Material

**ELN label:** HZB Battery: Electrode Material · **Class:** `ElectrodeMaterial`

An active or auxiliary electrode material, either synthesized in the lab or bought
(e.g. NMC111, graphite, carbon black).

| Field | Unit | Description |
|---|---|---|
| **name** | | Name of the material. |
| **synthesis** | | Synthesis from chemicals: steps, instruments and publication references (DOI, paper URL). |
| **precursor materials** | | Electrode materials this material was derived from by processing. See [Precursors and processing](reference_model.md#derived-from-another-entry-precursors-and-processing). |
| **processing** | | How **this** material was obtained from its precursors: steps and instruments. Only filled in the derived material, not in the precursor. |
| **yield** | % | Synthesis yield. |
| **volume and weights** | mL, g | Volume and mass of the batch. |
| **elemental composition** | | Elements of the material. |
| **chemicals** | | Chemicals used for the synthesis, with role and amount. |
| **product info / supplier** | | For bought materials. |

**Synthesis or processing?**

- *Synthesis* makes a new material from chemicals.
- *Processing* changes an existing electrode material, e.g. sieving or spray drying into
  a coarse, a medium and a fine fraction. Each fraction becomes its own new electrode
  material with the original material as precursor.

!!! tip "Processing is always described in the new entry"
    Precursors and processing are filled in the **new** entry (e.g. the fine fraction),
    not in the original material. They describe how this new material was obtained from
    its precursor. The original entry stays unchanged. See
    [Precursors and processing](reference_model.md#derived-from-another-entry-precursors-and-processing)
    for the step-by-step workflow.

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeMaterial
  name: NMC111_200um
  yield_percent: 0.95
  elemental_composition:
    - element: Li
    - element: Ni
    - element: Mn
    - element: Co
    - element: O
  synthesis:
    name: milling
    steps:
      - name: milling with 200 um beads
        duration: 3600
```

---

## Electrode Sheet

**ELN label:** HZB Battery: Electrode Sheet · **Class:** `ElectrodeSheet`

A cast or coated electrode sheet, made from electrode materials (active material, binder,
conductive agent, current collector, ...). Electrode samples are punched from it.

| Field | Unit | Description |
|---|---|---|
| **name** | | Name of the sheet. |
| **casting procedure** | | E.g. doctor blade casting, spray coating, dip coating, printing, dry casting, roll casting. Free text is allowed. |
| **dimensions and weights** | µm, g | Thickness, mass and shape of the sheet. |
| **elemental composition** | | Additional elements of the sheet. |
| **chemicals** | | Chemicals used directly, e.g. the solvent of the slurry. |
| **electrode materials** | | The electrode materials in the sheet, each with **role** (active material, binder, conductive agent, additive, current collector), **mass** (mg) and **wt%**. |
| **product info / supplier** | | For bought sheets. |

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet
  name: NMC111_sheet_01
  casting_procedure: Doctor blade casting
  dimensions_and_weights:
    thickness: 80
  electrode_materials:
    - material: '../upload/archive/mainfile/NMC111_200um.archive.yaml#data'
      role: active material
      wt_percent: 90
    - material: '../upload/archive/mainfile/PVDF.archive.yaml#data'
      role: binder
      wt_percent: 5
    - material: '../upload/archive/mainfile/carbon_black.archive.yaml#data'
      role: conductive agent
      wt_percent: 5
```

---

## Electrolyte Stock

**ELN label:** HZB Battery: Electrolyte Stock · **Class:** `ElectrolyteStock`

An electrolyte batch, mixed from salts and solvents in the lab or bought (e.g. LP30).

| Field | Unit | Description |
|---|---|---|
| **name** | | Name of the electrolyte. |
| **state** | | `Liquid` (default) or `Solid`. |
| **precursor electrolyte stocks** | | Electrolyte stocks this stock was derived from, e.g. by drying or adding an additive. |
| **processing** | | How **this** stock was obtained from its precursors. Only filled in the derived stock, not in the precursor. |
| **volume and weights** | mL, g | Volume and mass of the batch. |
| **elemental composition** | | Elements of the electrolyte. |
| **chemicals** | | Salts, solvents and additives with role, amount and concentration. |
| **product info / supplier** | | For bought electrolytes. |

An electrolyte stock has no `synthesis` section: mixing is documented through the
chemicals and their concentrations.

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_package.ElectrolyteStock
  name: LP30
  state: Liquid
  elemental_composition:
    - element: Li
    - element: P
    - element: F
    - element: C
    - element: H
    - element: O
```

---

## Separator Stock

**ELN label:** HZB Battery: Separator Stock · **Class:** `SeparatorStock`

A separator material (e.g. a porous polymer film, glass fibre, a ceramic-coated film).
Separator samples are cut from it.

| Field | Unit | Description |
|---|---|---|
| **name** | | Name of the separator. |
| **synthesis** | | Synthesis from chemicals, e.g. extrusion. |
| **precursor separator stocks** | | Separator stocks this stock was derived from, e.g. by coating. |
| **processing** | | How **this** stock was obtained from its precursors. Only filled in the derived stock, not in the precursor. |
| **dimensions and weights** | µm, g | Thickness, mass and shape. The thickness is passed on to the separator samples. |
| **elemental composition** | | Elements of the separator. |
| **chemicals** | | Chemicals used. |
| **product info / supplier** | | For bought separators. |

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_package.SeparatorStock
  name: Celgard_2400
  elemental_composition:
    - element: C
    - element: H
  synthesis:
    name: extrusion
```

---

## Electrode Sample

**ELN label:** HZB Battery: Electrode Sample · **Class:** `ElectrodeSample`

A piece cut or punched from an electrode sheet, ready to go into a cell.

| Field | Unit | Description |
|---|---|---|
| **name** | | Name of the sample. |
| **electrode sheet** | | The sheet the sample was cut from. |
| **dimensions and weights** | µm, g | Thickness, mass and shape (circle, rectangle or other) of the sample. |
| **chemicals** | | Chemicals used directly on the sample. |
| **product info / supplier** | | For bought electrodes. |

If no thickness is entered, the sample takes the thickness of its electrode sheet.

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSample
  name: NMC111_sheet_01_disc_03
  electrode_sheet: '../upload/archive/mainfile/NMC111_sheet_01.archive.yaml#data'
  dimensions_and_weights:
    mass: 0.012
    shape:
      m_def: nomad_battery_space.schema_packages.utilities.geometry.CircleGeometry
      diameter: 12
```

---

## Electrolyte Sample

**ELN label:** HZB Battery: Electrolyte Sample · **Class:** `ElectrolyteSample`

The amount of electrolyte taken from an electrolyte stock for one cell.

| Field | Unit | Description |
|---|---|---|
| **name** | | Name of the sample. |
| **electrolyte stock** | | The stock the electrolyte was taken from. |
| **volume and weights** | mL, g | Dosed volume and mass. |
| **product info / supplier** | | For bought electrolytes. |

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_package.ElectrolyteSample
  name: LP30_cell_01
  electrolyte_stock: '../upload/archive/mainfile/LP30.archive.yaml#data'
  volume_and_weights:
    volume: 0.08
```

---

## Separator Sample

**ELN label:** HZB Battery: Separator Sample · **Class:** `SeparatorSample`

A piece cut from a separator stock for one cell.

| Field | Unit | Description |
|---|---|---|
| **name** | | Name of the sample. |
| **separator stock** | | The stock the separator was cut from. |
| **dimensions and weights** | µm, g | Thickness, mass and shape of the sample. |
| **product info / supplier** | | For bought separators. |

If no thickness is entered, the sample takes the thickness of its separator stock.

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_package.SeparatorSample
  name: Celgard_2400_disc_01
  separator_stock: '../upload/archive/mainfile/Celgard_2400.archive.yaml#data'
  dimensions_and_weights:
    shape:
      m_def: nomad_battery_space.schema_packages.utilities.geometry.CircleGeometry
      diameter: 16
```

---

## Related pages

- [Links between entries](reference_model.md): how these entries are connected.
- [Battery Cells](cell_assembly_types.md): how samples are combined into a cell.
- [Reference](../reference/references.md): shared sections like chemicals, product info and geometry.
