"""
AIfund 是基于 Python 的基金量化工具
"""

from . import version
__version__ = version.version

name = "aifund"
__author__ = "tiano"

from aifund.data.fund_etf_em import (
    get_code,
    stock_realtime,
    realtime_data,
    web_data,
    market_realtime,
)

from fundstats.metrics import full

