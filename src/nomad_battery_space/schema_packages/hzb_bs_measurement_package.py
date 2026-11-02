#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Battery Measurement Package

Generic measurement entry: raw data files of any format (.dta, .nxs, ...)
attached to one or more battery samples. The files are only stored, not parsed.

NOMAD's `Measurement.samples` only accepts `CompositeSystem` entries, but all
battery samples are `ELNSubstance` (-> `PureSubstance` -> `System`). Therefore
`samples` is overridden with `BS_SampleReference`, which accepts any `System`.
"""

from baseclasses import BaseMeasurement
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.basesections.v1 import (
    CompositeSystemReference,
    System,
)
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

m_package = SchemaPackage()


class BS_SampleReference(CompositeSystemReference):
    """
    Reference to the measured sample. Accepts all battery samples (electrode
    materials, sheets, electrolytes, separators, cells, ...).

    Instead of selecting the entry, the sample ID (`lab_id`) can be entered;
    the reference is then resolved on save (see `EntityReference`).
    """

    m_def = Section(label='Sample')

    reference = Quantity(
        type=System,
        description='The measured sample.',
        a_eln={
            'component': 'ReferenceEditQuantity',
            'label': 'Sample',
            'showSectionLabel': True,
        },
    )


class BS_Measurement(BaseMeasurement, EntryData):
    """
    A measurement on battery samples with its raw data files.
    """

    m_def = Section(
        label='HZB Battery: Measurement',
        a_eln={
            'label': 'HZB Battery: Measurement',
            'hide': [
                'lab_id',
                'location',
                'end_time',
                'steps',
                'instruments',
                'results',
            ],
            'properties': {
                'order': [
                    'name',
                    'datetime',
                    'operator',
                    'method',
                    'data_file',
                    'description',
                    'samples',
                ],
            },
        },
    )

    data_file = Quantity(
        type=str,
        shape=['*'],
        description='Raw data files of the measurement (any format).',
        a_eln={'component': 'FileEditQuantity', 'label': 'Data files'},
        a_browser={'adaptor': 'RawFileAdaptor'},
    )

    samples = SubSection(
        section_def=BS_SampleReference,
        repeats=True,
        description='The samples measured in this measurement.',
    )


m_package.__init_metainfo__()
