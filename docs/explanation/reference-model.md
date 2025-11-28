# Battery Space Plugin – Reference Model

This NOMAD plugin defines independent ELN entries for:

- `Anode`
- `Cathode`
- `Electrolyte`
- `Separator`

Battery samples do not embed these components. Instead they use reference quantities inside a `Components` grouping section:

```python
class Components(ArchiveSection):
    anode_q = Quantity(type=Reference(Anode.m_def))
    cathode_q = Quantity(type=Reference(Cathode.m_def))
    electrolyte_q = Quantity(type=Reference(Electrolyte.m_def))
    separator_q = Quantity(type=Reference(Separator.m_def))
```


## Creating a battery sample

The user first creates standalone component entries:

- Anode → mass, area, …
- Cathode → mass, active_material, …
- Electrolyte → mass, volume, state, …
- Separator → thickness, …

Then the BatterySample references them:
```
components:
  anode_q: "#/anode_01"
  cathode_q: "#/cathode_01"
  electrolyte_q: "#/electrolyte_01"
  separator_q: "#/separator_01"
```
Normalization does not modify the references.

## Testing strategy

Because plugin tests run without the NOMAD processing backend, dereferencing is not supported. Tests therefore validate:

- the structure of BatterySample
- the presence and correctness of reference quantities 
- metadata such as sample_id

See ``tests/schema_packages/test_schema_package.py`` for a complete example.