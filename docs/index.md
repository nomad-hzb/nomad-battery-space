# Welcome to the `nomad-battery-space` documentation

A NOMAD plugin for documenting battery research at HZB.

## Introduction

`nomad-battery-space` provides ELN entries for the whole preparation chain of a battery
cell: from purchased chemicals, via synthesized electrode materials, cast electrode
sheets, electrolyte and separator stocks, to the electrode, electrolyte and separator
samples that are assembled into a cell. Measurement data can be attached to every step.

All entries are linked, so each cell can be traced back to the materials it was made
from, and cells can be searched by the chemical elements of their components.

<div markdown="block" class="home-grid">
<div markdown="block">

### Tutorial

Step-by-step guides for registering samples in the HZB NOMAD Oasis:

- [Tutorial](tutorial/tutorial.md)

</div>
<div markdown="block">

### How-to guides

How-to guides provide step-by-step instructions for a wide range of tasks, with the overarching topics:

- [Install this plugin](how_to/install_this_plugin.md)
- [Use this plugin](how_to/use_this_plugin.md)
- [Contribute to this plugin](how_to/contribute_to_this_plugin.md)

</div>

<div markdown="block">

### Data Model Explanation

How the entries of this plugin are structured and connected:

- [Overview](explanation/overview.md)
- [Materials and Components](explanation/component_types.md)
- [Links between Entries](explanation/reference_model.md)
- [Battery Cells](explanation/cell_assembly_types.md)
- [Measurements](explanation/measurements.md)

</div>
<div markdown="block">

### Reference

The [reference](reference/references.md) lists all entry types, shared sections, schema
packages and apps of this plugin.

</div>
</div>
