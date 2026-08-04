import os
from typing import TYPE_CHECKING

from baseclasses.voila import VoilaNotebook
from nomad.datamodel.data import EntryData
from nomad.metainfo import (
    Quantity,
    SchemaPackage,
    Section,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

m_package = SchemaPackage()


class BS_VoilaNotebook(VoilaNotebook, EntryData):
    """
    Voila Notebook for batch sample uploads.

    Extends VoilaNotebook for uploading battery samples in batch.
    """

    m_def = Section(a_eln=dict(hide=['lab_id']))

    file_uri = Quantity(
        type=str,
        description='URI to the notebook file in the file browser',
    )

    def get_file_uri(self, upload_id):
        if self.notebook_file is None:
            return None
        uri = f'nomad-oasis/gui/user/uploads/upload/id/{upload_id}/{self.notebook_file}'
        return uri

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        upload_id = archive.metadata.upload_id
        self.file_uri = self.get_file_uri(upload_id)

        if self.notebook_file and os.path.splitext(self.notebook_file)[-1] != '.ipynb':
            logger.error('Please upload a jupyter notebook file (.ipynb).')


# ============================================================================
# PACKAGE INITIALIZATION
# ============================================================================

m_package.__init_metainfo__()
