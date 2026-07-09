from typing import TYPE_CHECKING

from baseclasses.voila import VoilaNotebook
from nomad.datamodel.data import EntryData
from nomad.metainfo import Section

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


class BS_VoilaNotebook(VoilaNotebook, EntryData):
    """
    Voila Notebook for batch sample uploads.
    
    Extends VoilaNotebook for uploading battery samples in batch.
    """

    m_def = Section(a_eln=dict(hide=['lab_id']))

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
