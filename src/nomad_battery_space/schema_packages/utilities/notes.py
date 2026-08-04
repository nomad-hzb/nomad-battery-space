from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage, Section

m_package = SchemaPackage()


class Notes(ArchiveSection):
    """
    Section for storing notes related to a component or experiment.
    """

    m_def = Section(
        label='Notes',
        a_eln=dict(
            overview=True,
        ),
    )

    description = Quantity(
        type=str,
        description="""
        A field for adding additional information about the substance that is not captured
        by the other quantities and subsections.
        """,
        a_eln=dict(
            component='RichTextEditQuantity',
            label='detailed substance description',
        ),
    )


# ============================================================================
# PACKAGE INITIALIZATION
# ============================================================================

m_package.__init_metainfo__()
