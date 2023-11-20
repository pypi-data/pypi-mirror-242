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

from logging import getLogger
from typing import Iterable

from pandas import Series
from statsmodels.regression.linear_model import RegressionResultsWrapper

from f4ratk.analyze.api import EvaluatedResult
from f4ratk.analyze.regression import ModelType, Result
from f4ratk.history import AnnualizedReturns

log = getLogger(__name__)


class Critic:
    def evaluate(
        self, result: Result, historic_returns: AnnualizedReturns
    ) -> EvaluatedResult:
        log.debug(f"Evaluating with: {historic_returns}")

        factors = self._normalize(
            self._significant_factors(
                result.model, Critic._target_factors(result.model_type)
            )
        )
        expectation = self._expectation(historic_returns)

        forecast = factors.mul(expectation).sum()

        return Critic._wrap(result=result, evaluation=forecast)

    def _significant_factors(
        self, model: RegressionResultsWrapper, target_factors: Iterable[str]
    ) -> Series:
        targeted = model.params[target_factors]
        return targeted[model.pvalues < 0.1]

    def _normalize(self, factors: Series) -> Series:
        if 'MKT' in factors:
            factors['MKT'] -= 1
        return factors

    def _expectation(self, historic_returns: AnnualizedReturns) -> Series:
        return historic_returns.all().div(2)

    @staticmethod
    def _target_factors(model_type: ModelType) -> Iterable[str]:
        if model_type == ModelType.CAPM:
            return ['MKT']
        elif model_type == ModelType.FF3:
            return ['MKT', 'SMB', 'HML']
        elif model_type == ModelType.FF5:
            return ['MKT', 'SMB', 'HML', 'RMW', 'CMA']
        elif model_type == ModelType.FF6:
            return ['MKT', 'SMB', 'HML', 'RMW', 'CMA', 'WML']
        else:
            raise ValueError

    @staticmethod
    def _wrap(result: Result, evaluation: float) -> EvaluatedResult:
        return EvaluatedResult(
            model_type=result.model_type, model=result.model, evaluation=evaluation
        )
