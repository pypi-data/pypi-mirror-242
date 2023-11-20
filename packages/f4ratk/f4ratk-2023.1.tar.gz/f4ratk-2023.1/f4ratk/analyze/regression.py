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
from typing import Iterable, Tuple

import pandas
from pandas import DataFrame
from statsmodels.formula import api as sm
from statsmodels.regression.linear_model import RegressionResultsWrapper

from f4ratk.analyze.api import FundReturns, ModelType
from f4ratk.shared import first_period, last_period

log = getLogger(__name__)


@dataclass(frozen=True)
class Configuration:
    model_type: ModelType
    formula: str

    @staticmethod
    def of(model_type: ModelType) -> "Configuration":
        if model_type == ModelType.CAPM:
            return Configuration(model_type, 'XsRet ~ MKT')
        elif model_type == ModelType.FF3:
            return Configuration(model_type, 'XsRet ~ MKT + SMB + HML')
        elif model_type == ModelType.FF5:
            return Configuration(model_type, 'XsRet ~ MKT + SMB + HML + RMW + CMA')
        elif model_type == ModelType.FF6:
            return Configuration(
                model_type, 'XsRet ~ MKT + SMB + HML + RMW + CMA + WML'
            )
        else:
            raise ValueError


@dataclass(frozen=True)
class Result:
    model_type: ModelType
    model: RegressionResultsWrapper


class RegressionRunner:
    def run(
        self,
        configurations: Iterable[Configuration],
        returns: FundReturns,
        fama_data: DataFrame,
    ) -> Tuple[Result]:
        combined = self._combine(returns, fama_data)

        return tuple(
            self._run(configuration=configuration, data=combined)
            for configuration in configurations
        )

    def _combine(self, returns: FundReturns, fama_data: DataFrame) -> DataFrame:
        log.info(
            f"Returns data range: {returns.first_period()} - {returns.last_period()}"
        )
        log.info(
            f"Fama data range : {first_period(fama_data)} - {last_period(fama_data)}"
        )

        combined: DataFrame = pandas.merge(
            returns.data, fama_data, left_index=True, right_index=True
        )

        combined['XsRet'] = combined[FundReturns.DATA_COLUMN_NAME] - combined['RF']

        log.info(
            f"Result date range: {first_period(combined)} - {last_period(combined)}"
        )

        return combined

    def _run(self, configuration: Configuration, data: DataFrame) -> Result:
        model = self._model(formula=configuration.formula, data=data)
        return Result(model_type=configuration.model_type, model=model)

    def _model(self, formula: str, data: DataFrame) -> RegressionResultsWrapper:
        return sm.ols(formula=formula, data=data).fit(
            cov_type='HAC', cov_kwds={'maxlags': None}, use_t=True
        )
