import os

from nomad.client import normalize_all, parse

import os
import shutil
from nomad.processing import process
from nomad.datamodel.context import ServerContext


def load_upload(directory):
    # Process an entire folder as one upload
    upload = process(directory)

    # Build server-like context for resolving references
    ctx = ServerContext(upload)

    # Each processed archive is inside upload.processed
    archives = [a for a in upload.processed]

    return ctx, archives

def test_schema_package(tmp_path):
    data_dir = tmp_path / "upload"
    data_dir.mkdir()

    # Copy files into temporary upload folder
    for fname in [
        "anode.archive.yaml",
        "cathode.archive.yaml",
        "electrolyte.archive.yaml",
        "separator.archive.yaml",
        "battery_sample.archive.yaml",
    ]:
        shutil.copy(os.path.join("tests", "data", fname), data_dir / fname)

    # Process the upload with NOMAD 1.x pipeline
    ctx, archives = load_upload(data_dir)

    # Find the battery archive
    battery = next(a for a in archives if a.data.m_def.name == "BatterySample")

    # Resolve references using ServerContext
    anode = ctx.resolve(battery.data.components.anode_q)
    cathode = ctx.resolve(battery.data.components.cathode_q)
    electrolyte = ctx.resolve(battery.data.components.electrolyte_q)
    separator = ctx.resolve(battery.data.components.separator_q)

    # Assertions
    assert battery.data.name == "bat_01"
    assert anode.mass.magnitude == 1.2
    assert cathode.mass_active_material.magnitude == 2.1
    assert electrolyte.volume.magnitude == 1.1
    assert separator.thickness.magnitude == 20.0
    assert battery.data.sample_identifiers.sample_id == "ABC123"
