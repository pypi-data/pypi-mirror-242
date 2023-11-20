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

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from pandas import DataFrame, Period
from statsmodels.regression.linear_model import RegressionResultsWrapper

from f4ratk.domain import ModelType
from f4ratk.history import AnnualizedReturns
from f4ratk.shared import first_period, format_range, last_period


@dataclass(init=False, frozen=True, eq=False)
class FundReturns:
    DATA_COLUMN_NAME = "Returns"

    data: DataFrame

    def __init__(self, data: DataFrame):
        if (data is None) or (FundReturns.DATA_COLUMN_NAME not in data.columns):
            raise ValueError
        object.__setattr__(self, "data", data)

    def first_period(self) -> Period:
        return first_period(self.data)

    def last_period(self) -> Period:
        return last_period(self.data)

    def formatted_range(self) -> str:
        return format_range(self.data)

    def __eq__(self, other) -> bool:
        return isinstance(other, FundReturns) and self.data.equals(other.data)

    def weighted(self, weight: float):
        return FundReturns(data=self.data.mul(weight))


@dataclass(frozen=True)
class EvaluatedResult:
    model_type: ModelType
    model: RegressionResultsWrapper
    evaluation: float


@dataclass(frozen=True)
class EvaluatedResults:
    _results: [ModelType, EvaluatedResult]

    def __getitem__(self, key: ModelType) -> EvaluatedResult:
        return self._results[key]

    @staticmethod
    def of(results: Iterable[EvaluatedResult]):
        return EvaluatedResults(
            _results={result.model_type: result for result in results}
        )


class DataAnalyzer(metaclass=ABCMeta):
    @abstractmethod
    def analyze(
        self,
        models: Iterable[ModelType],
        returns: FundReturns,
        fama_data: DataFrame,
        historic_returns: AnnualizedReturns,
    ) -> EvaluatedResults:
        """Analyze data in regards to fit for Fama / French models."""
