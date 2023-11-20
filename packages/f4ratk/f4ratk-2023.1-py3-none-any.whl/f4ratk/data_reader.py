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

import random
from datetime import date, timedelta
from typing import Optional

from pandas_datareader.famafrench import FamaFrenchReader
from pandas_datareader.fred import FredReader
from requests_cache import CachedSession
from urllib3 import Retry
from yahooquery import Ticker
from yahooquery.utils import (
    DEFAULT_TIMEOUT,
    USER_AGENT_LIST,
    TimeoutHTTPAdapter,
    headers,
)

from f4ratk.directories import cache


def _cached_session() -> CachedSession:
    cache_duration = timedelta(days=14)
    cache_location = str(cache.file(name='requests'))

    session = CachedSession(
        cache_name=cache_location, backend='sqlite', expire_after=cache_duration
    )
    session.remove_expired_responses()

    return session


def _cached_yahoo_session() -> CachedSession:
    """Configure specific headers

    We have to borrow from yahooquery.utils.__init__._init_session until
    passing a cached session to original configuration will be possible.
    """

    session = _cached_session()

    session_headers = headers
    retries = Retry(
        total=5,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    session.mount(
        "https://",
        TimeoutHTTPAdapter(max_retries=retries, timeout=DEFAULT_TIMEOUT),
    )
    session_headers["User-Agent"] = random.choice(USER_AGENT_LIST)
    session.headers.update(**session_headers)
    return session


_session = _cached_yahoo_session()


def yahoo_reader(ticker_symbol: str) -> Ticker:
    return Ticker(ticker_symbol, session=_session)


def fama_french_reader(returns_data: str) -> FamaFrenchReader:
    return FamaFrenchReader(symbols=returns_data, session=_session, start='1920')


def fred_reader(
    exchange_symbol: str, start: Optional[date], end: Optional[date]
) -> FredReader:
    return FredReader(
        symbols=exchange_symbol,
        start=start if start else '1970',
        end=end,
        session=_session,
    )
