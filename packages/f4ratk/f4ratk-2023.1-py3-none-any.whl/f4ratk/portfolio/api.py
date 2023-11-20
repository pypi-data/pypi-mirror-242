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

from f4ratk.analyze.api import EvaluatedResults
from f4ratk.portfolio.ports import PortfolioRequest


class PortfolioAnalyzer(metaclass=ABCMeta):
    @abstractmethod
    def analyze_portfolio_file(self, request: PortfolioRequest) -> EvaluatedResults:
        """Analyze a portfolio in a configuration file."""
