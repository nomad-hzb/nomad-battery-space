# Measurements

**ELN label:** HZB Battery: Measurement · **Class:** `BS_Measurement`

A measurement entry stores the raw data files of a measurement and links them to the
measured samples. Any file format can be uploaded (e.g. `.dta`, `.nxs`, `.txtr`). The files
are stored as they are; their content is not read by the plugin.

| Field | Description |
|---|---|
| **name** | Name of the measurement. |
| **datetime** | Date and time of the measurement. |
| **operator** | Person who did the measurement. |
| **method** | Measurement method, e.g. galvanostatic cycling. |
| **data files** | One or more raw data files of any format. |
| **description** | Free text. |
| **samples** | The measured samples. |

## Which samples can be measured

The **samples** list accepts every entry of the plugin: chemicals, electrode materials,
electrode sheets, stocks, samples and cells. Intermediates created by
[processing](reference_model.md#derived-from-another-entry-precursors-and-processing)
can therefore be measured, too.

A sample can be linked in two ways:

- **Select the entry** in the reference field. This is the recommended way: you see which
  entry you link.
- **Enter its lab ID.** The matching entry is looked up when the measurement is saved.
  This is useful if you know the ID but do not want to search the list, e.g. when
  creating measurements from YAML files.

When you enter a lab ID, check the result after saving:

- The sample entry must already exist and have this lab ID. If no entry is found, the
  reference stays empty.
- If several entries have the same lab ID, the first one found is used. Which one that
  is cannot be predicted, so select the entry from the list in this case.

A measurement can also be saved without samples and linked later.

```yaml
data:
  m_def: nomad_battery_space.schema_packages.hzb_bs_measurement_package.BS_Measurement
  name: cell_01 cycling
  datetime: 2026-01-20T09:00:00Z
  method: galvanostatic cycling
  operator: Jane Doe
  data_file:
    - cell_01_cycling.dta
    - cell_01_operando.nxs
  samples:
    - lab_id: CC_001
```

The data files must be part of the same upload.
