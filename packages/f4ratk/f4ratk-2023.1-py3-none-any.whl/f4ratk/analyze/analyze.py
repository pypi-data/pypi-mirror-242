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

from typing import Iterable

from pandas import DataFrame

from f4ratk.analyze.api import DataAnalyzer, EvaluatedResults, FundReturns, ModelType
from f4ratk.analyze.evaluation import Critic
from f4ratk.analyze.regression import Configuration, RegressionRunner
from f4ratk.history import AnnualizedReturns


class DataAnalyzerAdapter(DataAnalyzer):
    def __init__(self, regression_runner: RegressionRunner, critic: Critic):
        self._regression_runner = regression_runner
        self._critic = critic

    def analyze(
        self,
        models: Iterable[ModelType],
        returns: FundReturns,
        fama_data: DataFrame,
        historic_returns: AnnualizedReturns,
    ) -> EvaluatedResults:
        regression_results = self._regression_runner.run(
            configurations=[Configuration.of(model_type) for model_type in models],
            returns=returns,
            fama_data=fama_data,
        )

        evaluated_results = EvaluatedResults.of(
            self._critic.evaluate(regression, historic_returns)
            for regression in regression_results
        )

        return evaluated_results
