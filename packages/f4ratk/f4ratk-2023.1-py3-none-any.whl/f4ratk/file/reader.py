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
from os import PathLike
from typing import Optional

from pandas import DataFrame, merge, read_csv

from f4ratk.analyze.api import FundReturns
from f4ratk.domain import Currency, Frame, Frequency
from f4ratk.exchange import ExchangeReader
from f4ratk.file.api import FileConfig, FileReader, ValueFormat
from f4ratk.shared import Normalizer


class CsvFileReader:
    _HEADER = ('Dates', 'Returns')

    def __init__(self, path: PathLike):
        self._path = path

    def read(self) -> DataFrame:
        return read_csv(self._path, parse_dates=True, index_col=0, names=self._HEADER)


class FileContentReader:
    def __init__(
        self,
        csv_reader: CsvFileReader,
        exchange_reader: ExchangeReader,
        currency: Currency,
        value_format: ValueFormat,
        normalizer: Normalizer,
    ):
        self._csv_reader = csv_reader
        self._exchange_reader = exchange_reader
        self._currency = currency
        self._value_format = value_format
        self._normalizer = normalizer

    def read(
        self, start: Optional[date], end: Optional[date], frequency: Frequency
    ) -> FundReturns:
        data = self._csv_reader.read().sort_index().truncate(start, end)

        data = self._normalizer.index_to_periods(data=data, frequency=frequency)

        if self._currency is not Currency.USD:
            data = self._convert_currency(
                data=data, currency=self._currency, start=start, end=end
            )

        if self._value_format == ValueFormat.PRICE:
            data = data[['Returns']].pct_change() * 100

        return FundReturns(data=data.dropna())

    def _convert_currency(
        self, data: DataFrame, currency: Currency, start: date, end: date
    ) -> DataFrame:
        exchange_data = self._exchange_reader.exchange_data(currency, start, end)

        data = merge(data, exchange_data, left_index=True, right_index=True)

        data['Returns'] = data['Returns'] * data[ExchangeReader.EXCHANGE_RATE_COLUMN]

        return data[['Returns']]


class FileReaderAdapter(FileReader):
    def __init__(self, normalizer: Normalizer):
        self._normalizer = normalizer

    def read(self, file_config: FileConfig, frame: Frame) -> FundReturns:
        file_reader = FileContentReader(
            csv_reader=CsvFileReader(path=file_config.path),
            exchange_reader=ExchangeReader(frame.frequency),
            currency=file_config.currency,
            value_format=file_config.value_format,
            normalizer=self._normalizer,
        )

        return file_reader.read(
            start=frame.start, end=frame.end, frequency=frame.frequency
        )
