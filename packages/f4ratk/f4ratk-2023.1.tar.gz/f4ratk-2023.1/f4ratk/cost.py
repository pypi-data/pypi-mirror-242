##############################################################################
# Copyright (C) 2020 - 2023 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of f4ratk.
#
# f4ratk is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from dataclasses import dataclass
from logging import getLogger
from typing import Iterable, Optional, Union

log = getLogger(__name__)


@dataclass(frozen=True)
class Statements:
    total_expense_ratio: float
    expenses: int

    transaction_costs: Optional[int]
    withholding_tax: Optional[int]
    capital_gains_tax: Optional[int]

    securities_lending_income: Optional[int]


@dataclass(frozen=True)
class CostIncreases:
    total_expense_ratio: float
    withholding_tax_ratio: Optional[float]
    capital_gains_tax_ratio: Optional[float]
    transaction_costs_ratio: Optional[float]


@dataclass(frozen=True)
class CostDecreases:
    securities_lending_ratio: Optional[float]


@dataclass(frozen=True)
class CostBreakdown:
    increases: CostIncreases
    decreases: CostDecreases

    total_costs_ratio: float


class Accountant:
    @staticmethod
    def assess(statements: Statements) -> CostBreakdown:
        estimated_mean_net_asset_ratio = (
            statements.expenses / statements.total_expense_ratio
        )

        increases = Accountant._cost_increases(
            estimated_mean_net_asset_ratio=estimated_mean_net_asset_ratio,
            total_expense_ratio=statements.total_expense_ratio,
            withholding_tax=statements.withholding_tax,
            capital_gains_tax=statements.capital_gains_tax,
            transaction_costs=statements.transaction_costs,
        )

        decreases = CostDecreases(
            securities_lending_ratio=statements.securities_lending_income
            / estimated_mean_net_asset_ratio
            if statements.securities_lending_income and estimated_mean_net_asset_ratio
            else None
        )

        total_costs_ratio = Accountant._total_costs(increases, decreases)

        return CostBreakdown(increases, decreases, total_costs_ratio)

    @staticmethod
    def _cost_increases(
        estimated_mean_net_asset_ratio: float,
        total_expense_ratio: float,
        withholding_tax: Optional[int],
        capital_gains_tax: Optional[int],
        transaction_costs: Optional[int],
    ) -> CostIncreases:
        return CostIncreases(
            total_expense_ratio=total_expense_ratio,
            withholding_tax_ratio=withholding_tax / estimated_mean_net_asset_ratio
            if withholding_tax and estimated_mean_net_asset_ratio
            else None,
            capital_gains_tax_ratio=capital_gains_tax / estimated_mean_net_asset_ratio
            if capital_gains_tax and estimated_mean_net_asset_ratio
            else None,
            transaction_costs_ratio=transaction_costs / estimated_mean_net_asset_ratio
            if transaction_costs and estimated_mean_net_asset_ratio
            else None,
        )

    @staticmethod
    def _total_costs(increases: CostIncreases, decreases: CostDecreases):
        sum_increases = Accountant._sum_ignore_missing(
            (
                increases.total_expense_ratio,
                increases.withholding_tax_ratio,
                increases.capital_gains_tax_ratio,
                increases.transaction_costs_ratio,
            )
        )

        sum_decreases = Accountant._sum_ignore_missing(
            (decreases.securities_lending_ratio,)
        )

        return sum_increases - sum_decreases

    @staticmethod
    def _sum_ignore_missing(elements: Iterable[Optional[Union[int, float]]]) -> float:
        return sum(filter(lambda x: x is not None, elements))
