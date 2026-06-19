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
Coin Cell Battery Package

This module implements the specific data model for coin cell batteries,
extending the generalized BatterySample with coin cell-specific parameters
like case type and crimping method.
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
from .utils import create_string_quantity

m_package = SchemaPackage()


class CoinCellBattery(BatterySample):
    """
    Coin cell battery assembly with specific coin cell parameters.
    
    This extends BatterySample with coin cell-specific assembly parameters
    like case type (IEC 60086 standard) and crimping method/pressure.
    
    Battery components (electrodes, separator, electrolyte) are inherited
    from the BatterySample base class.
    """
    m_def = Section(
        links=['https://w3id.org/emmo/domain/battery#battery_b7fdab58_6e91_4c84_b097_b06eff86a124'],
        label="HZB Battery: Coin Cell",
        a_eln={
            "label": "HZB Battery: Coin Cell",
            "entry_type": "CoinCell",
            "hide": ['pure_substance',"substance_identifiers", 'elemental_composition'],
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
                ],
                "order_default": [
                    "description",
                    "sample_identifiers",
                ]
            },
        },
    )

    # ---- Coin Cell Specific Parameters ----

    case_id = create_string_quantity(
        "Case-ID",
        description=(
            "Standardized coin cell housing code according to IEC 60086.\n\n"
            "Letters indicate the electrochemical system (e.g. CR = Li-MnO₂), "
            "followed by four digits: first two = nominal diameter (mm), "
            "last two = nominal height (0.1 mm).\n\n"
            "Example: CR2032 → 20 mm diameter, 3.2 mm height."
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
