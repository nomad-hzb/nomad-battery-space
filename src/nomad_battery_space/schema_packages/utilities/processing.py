"""
Generic sections for samples that were derived from other samples by processing.

"Processing" means an existing sample/material was physically changed (e.g.
milling, spray drying, calcination, coating) and the result is registered as a
new entry. This is different from "cut from / taken from" relations (e.g.
ElectrodeSample -> ElectrodeSheet), where the material itself is unchanged.

Usage: inherit `ProcessedFromMixin` and override `precursors` with a typed
reference, so that only samples of the same type can be selected:

    class ElectrodeMaterialReference(PrecursorReference):
        reference = Quantity(type=Reference(SectionProxy('ElectrodeMaterial')))

    class ElectrodeMaterial(ELNSubstance, ProcessedFromMixin):
        precursors = SubSection(section_def=ElectrodeMaterialReference, repeats=True)
"""

from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.basesections.v1 import (
    Entity,
    EntityReference,
    Process,
)
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

m_package = SchemaPackage()


class PrecursorReference(EntityReference):
    """
    Reference to the sample this sample was derived from by processing.

    Subclasses should narrow the type of `reference` to a specific sample class.
    The reference can also be resolved from the `lab_id` (see `EntityReference`).
    """

    m_def = Section(label='Precursor')

    reference = Quantity(
        type=Entity,
        description='The sample this sample was derived from.',
        a_eln=dict(component='ReferenceEditQuantity', label='precursor'),
    )


class SampleProcessing(Process):
    """
    The processing that turned the precursor(s) into this sample, with its
    steps and the instruments used.
    """

    m_def = Section(
        label='Processing',
        a_eln={
            'hide': ['samples'],
            'properties': {
                'order': [
                    'name',
                    'datetime',
                    'end_time',
                    'steps',
                    'instruments',
                    'description',
                ],
            },
        },
    )


class ProcessedFromMixin(ArchiveSection):
    """
    Adds the "derived from <precursors> by <processing>" relation to a sample class.
    """

    precursors = SubSection(
        section_def=PrecursorReference,
        repeats=True,
        description='Samples this sample was derived from by processing.',
    )
    processing = SubSection(
        section_def=SampleProcessing,
        description='How this sample was obtained from its precursors: steps and instruments.',
    )


# ============================================================================
# PACKAGE INITIALIZATION
# ============================================================================

m_package.__init_metainfo__()
