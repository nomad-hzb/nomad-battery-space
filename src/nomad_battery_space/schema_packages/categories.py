"""
Custom entry-data category for the HZB Battery Space schemas.

Schemas that list this category in their ``m_def = Section(categories=[...])``
are grouped under their own filter chip in the "Create entry" dialog.
"""

from nomad.datamodel.data import EntryDataCategory
from nomad.metainfo.metainfo import Category


class BatteryDataSpaceCategory(EntryDataCategory):
    m_def = Category(label='HZB Battery', categories=[EntryDataCategory])
