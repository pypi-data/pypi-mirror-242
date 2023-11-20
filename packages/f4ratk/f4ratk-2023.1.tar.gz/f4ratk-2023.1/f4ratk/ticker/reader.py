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

from datetime import date
from logging import getLogger
from typing import Callable, Optional

from pandas import DataFrame, merge, to_datetime
from yahooquery import Ticker

from f4ratk.analyze.api import FundReturns
from f4ratk.domain import Currency, Frame, Frequency
from f4ratk.exchange import ExchangeReader
from f4ratk.shared import Downsampler, Normalizer, QualityChecker
from f4ratk.ticker.api import NoTickerData, Stock, TickerReader

log = getLogger(__name__)


class TickerReaderAdapter(TickerReader):
    _ADJUSTED_CLOSE_COLUMN = 'adjclose'

    def __init__(
        self,
        yahoo_reader: Callable[[str], Ticker],
        normalizer: Normalizer,
        downsampler: Downsampler,
        quality_checker: Optional[QualityChecker] = None,
    ):
        self._yahoo_reader = yahoo_reader
        self._normalizer = normalizer
        self._downsampler = downsampler
        self._quality_checker = quality_checker

    def read_ticker(self, stock: Stock, frame: Frame) -> FundReturns:
        data = self._read_stock_data(stock, frame.start, frame.end)
        data = self._normalize_date_range(data, frame.frequency)

        if stock.currency is not Currency.USD:
            data = self._convert_currency(data, stock.currency, frame)

        data[
            FundReturns.DATA_COLUMN_NAME
        ] = self._calculate_returns_as_relative_percentage(data)

        log.debug(
            f"Stock data of symbol '{stock.ticker_symbol}' starts at: \n%s", data.head()
        )

        return FundReturns(data=data[[FundReturns.DATA_COLUMN_NAME]].dropna())

    def _read_stock_data(
        self, stock: Stock, start: Optional[date], end: Optional[date]
    ) -> DataFrame:
        try:
            data = self._yahoo_reader(stock.ticker_symbol).history(
                period="max", start=start if start else "1970", end=end
            )
            if not len(data):
                raise ValueError
            data.index = to_datetime(data.index.levels[1], utc=True)
        except Exception:
            log.exception("Exception while fetching yahoo data")
            raise NoTickerData(stock.ticker_symbol)
        return data

    def _convert_currency(
        self, data: DataFrame, currency: Currency, frame: Frame
    ) -> DataFrame:
        exchange_data = ExchangeReader(frequency=frame.frequency).exchange_data(
            currency, frame.start, frame.end
        )

        data = merge(data, exchange_data, left_index=True, right_index=True)

        source_currency_close_column = (
            f"{self._ADJUSTED_CLOSE_COLUMN} ({currency.name})"
        )

        data = data.rename(
            columns={self._ADJUSTED_CLOSE_COLUMN: source_currency_close_column}
        )

        data[self._ADJUSTED_CLOSE_COLUMN] = (
            data[source_currency_close_column]
            * data[ExchangeReader.EXCHANGE_RATE_COLUMN]
        )

        return data

    def _calculate_returns_as_relative_percentage(self, data: DataFrame) -> DataFrame:
        return data[[self._ADJUSTED_CLOSE_COLUMN]].pct_change() * 100

    def _normalize_date_range(self, data: DataFrame, frequency: Frequency) -> DataFrame:
        data = self._normalizer.index_to_periods(data=data, frequency=Frequency.DAILY)

        if self._quality_checker:
            self._quality_checker.investigate(data)

        if frequency == Frequency.MONTHLY:
            data = self._down_sample(data)

        return data

    def _down_sample(self, data: DataFrame) -> DataFrame:
        log.info("Downsampling ticker data to monthly rate")
        data = self._downsampler.monthly_sample(data=data)
        return data
