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

from pandas import DataFrame

from f4ratk.analyze.api import DataAnalyzer, EvaluatedResults, FundReturns
from f4ratk.domain import Frame, Frequency, Region
from f4ratk.fama import FamaReader
from f4ratk.file.api import FileReader
from f4ratk.file.reader import FileConfig
from f4ratk.history import History
from f4ratk.portfolio.api import PortfolioAnalyzer
from f4ratk.portfolio.ports import (
    Origin,
    PortfolioConfiguration,
    PortfolioReader,
    PortfolioRequest,
    Source,
)
from f4ratk.ticker.api import Stock, TickerReader

log = getLogger(__name__)


class PortfolioAnalyzerAdapter(PortfolioAnalyzer):
    def __init__(
        self,
        portfolio_reader: PortfolioReader,
        fama_reader: FamaReader,
        ticker_reader: TickerReader,
        file_reader: FileReader,
        analyzer: DataAnalyzer,
        history: History,
    ):
        self._portfolio_reader = portfolio_reader
        self._fama_reader = fama_reader
        self._ticker_reader = ticker_reader
        self._file_reader = file_reader
        self._analyzer = analyzer
        self._history = history

    def analyze_portfolio_file(self, request: PortfolioRequest) -> EvaluatedResults:
        portfolio = self._portfolio_reader.read(request=request)

        return self._analyze_portfolio(portfolio)

    def _analyze_portfolio(self, portfolio: PortfolioConfiguration) -> EvaluatedResults:
        frame = portfolio.config.frame
        region = portfolio.config.region

        portfolio_data = self._read_combined_sources(portfolio.sources, frame)

        fama_data = self._read_fama_data(region, frame.frequency)

        historic_returns = self._history.annualized_returns(region=region)

        return self._analyzer.analyze(
            portfolio.config.models,
            portfolio_data,
            fama_data,
            historic_returns,
        )

    def _read_combined_sources(
        self, sources: Iterable[Source], frame: Frame
    ) -> FundReturns:
        combined = sum(
            self._read_weighted_data(source, frame).data for source in sources
        )
        return FundReturns(data=combined.dropna())

    def _read_weighted_data(self, source: Source, frame: Frame) -> FundReturns:
        returns = self._read_returns(source.origin, frame)
        log.debug("Source data range: %s", returns.formatted_range())
        return returns.weighted(source.weight / 100)

    def _read_returns(self, origin: Origin, frame: Frame) -> FundReturns:
        if isinstance(origin, Stock):
            return self._ticker_reader.read_ticker(stock=origin, frame=frame)
        elif isinstance(origin, FileConfig):
            return self._file_reader.read(file_config=origin, frame=frame)

        raise ValueError

    def _read_fama_data(self, region: Region, frequency: Frequency) -> DataFrame:
        return self._fama_reader.fama_data(region=region, frequency=frequency)
