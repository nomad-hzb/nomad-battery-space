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
Battery Assembly Package

This module implements specific data models for assembled battery cells,
extending the generalized BatterySample with format-specific parameters
(e.g., coin cell, pouch cell, cylindrical cell). Each battery type includes
parameters specific to its assembly and form factor while inheriting
common components (electrodes, separator, electrolyte) from BatterySample.
"""

from typing import TYPE_CHECKING

from nomad.metainfo import (
    Enum,
    Quantity,
    SchemaPackage,
    Section,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from .hzb_bs_package import BatterySample

m_package = SchemaPackage()


class CoinCellBattery(BatterySample):
    """
    Coin cell battery assembly with specific coin cell parameters.
    
    This extends BatterySample with coin cell-specific assembly parameters
    like case type and crimping method/pressure.
    
    Battery components (electrodes, separator, electrolyte) are inherited
    from the BatterySample base class.
    """
    m_def = Section(
        links=['https://w3id.org/emmo/domain/battery#battery_b7fdab58_6e91_4c84_b097_b06eff86a124'],
        label="HZB Battery: Coin Cell",
        a_eln={
            "label": "HZB Battery: Coin Cell",
            "entry_type": "CoinCell",
            "hide": ['pure_substance','elemental_composition', 'description'],
            "properties": {
                "order": [
                    "lab_id",
                    "name",
                    "datetime",
                    "case_id",
                    "case_crimp",
                    "pressure",
                    "working_electrode",
                    "counter_electrode",
                    "reference_electrode",
                    "separator",
                    "electrolyte",
                    "product_info"
                ],
                "order_default": [
                    "substance_identifiers",
                ]
            },
        },
        a_template=dict(
            substance_identifiers=dict(),
        ),
    )

    # ---- Coin Cell Specific Parameters ----

    case_id = Quantity(
        type=str,
        description=(
            "Coin cell case identifier based on standardized or non-standardized dimensions.\n\n"
            "Enter the numeric code with first two digits indicating nominal diameter and last two digits indicating nominal height.\n"
            "- 2032: 20 mm diameter, 3.2 mm height.\n"
            "- 2025: 20 mm diameter, 2.5 mm height.\n"
            "- operando: self-constructed operando cells for in-situ measurements"
        ),
        a_eln=dict(
            label="case-id",
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '2032',
                    '2025',
                    'operando',
                ]
            ),
        ),
    )

    CaseCrimpEnum = Enum(["manual", "automatic"])
    case_crimp = Quantity(
        type=CaseCrimpEnum,
        default='manual',
        description="Method used to seal/crimp the coin cell case.",
        a_eln={"component": "EnumEditQuantity", "label": "case-crimp"}
    )

    pressure = Quantity(
        type=float,
        unit="MPa",
        description="Applied pressure during crimping (for automatic crimping).",
        a_eln={
            "component": "NumberEditQuantity",
            "label": "pressure (automatic only)",
            "defaultDisplayUnit": "MPa",
        },
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        
        super().normalize(archive, logger)
        
        # set pressure to None if manual crimping is used
        if self.case_crimp == "manual":
            self.pressure = None


m_package.__init_metainfo__()
