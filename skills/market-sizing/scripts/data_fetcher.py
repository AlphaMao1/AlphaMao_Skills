"""
Data helpers for market sizing.

This module helps find and fetch usable public data. It does not make a number
"true"; every value still needs a source card and a transformation note.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import urlopen

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - import guard
    raise ImportError("Please install pandas: pip install pandas") from exc

try:
    from fredapi import Fred

    FRED_AVAILABLE = True
except ImportError:
    FRED_AVAILABLE = False

try:
    import wbdata

    WBDATA_AVAILABLE = True
except ImportError:
    WBDATA_AVAILABLE = False

try:
    import akshare as ak

    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False

try:
    import yfinance as yf

    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    from pytrends.request import TrendReq

    PYTRENDS_AVAILABLE = True
except ImportError:
    PYTRENDS_AVAILABLE = False


SOURCE_CATALOG: Dict[str, Dict[str, str]] = {
    "world_bank": {
        "provider": "World Bank",
        "best_for": "population, GDP, macro indicators across countries",
        "endpoint": "https://api.worldbank.org/v2/",
        "notes": "No API key. Good baseline for country-level denominators.",
    },
    "fred": {
        "provider": "Federal Reserve Economic Data",
        "best_for": "US macro and financial time series",
        "endpoint": "https://fred.stlouisfed.org/docs/api/fred/",
        "notes": "Requires a free API key for package use.",
    },
    "dbnomics": {
        "provider": "DBnomics",
        "best_for": "aggregated public macro datasets from many providers",
        "endpoint": "https://api.db.nomics.world/v22/",
        "notes": "Useful discovery layer when provider-specific APIs are fragmented.",
    },
    "oecd": {
        "provider": "OECD",
        "best_for": "OECD structural, industry, education, labor, and policy indicators",
        "endpoint": "https://sdmx.oecd.org/public/rest/",
        "notes": "Use SDMX queries; record dataset and dimension filters in source cards.",
    },
    "imf": {
        "provider": "IMF",
        "best_for": "WEO, macro, finance, country and region comparisons",
        "endpoint": "https://www.imf.org/external/datamapper/api/",
        "notes": "DataMapper is convenient for indicators and country sets.",
    },
    "un_comtrade": {
        "provider": "UN Comtrade",
        "best_for": "trade, HS codes, import/export side checks",
        "endpoint": "https://comtradeapi.un.org/",
        "notes": "Good for hardware, commodity, equipment, and cross-border checks.",
    },
    "china_nbs": {
        "provider": "National Bureau of Statistics of China",
        "best_for": "China population, macro, industry output, retail, fixed asset data",
        "endpoint": "https://data.stats.gov.cn/",
        "notes": "Prefer original tables; AkShare can be a convenience wrapper.",
    },
    "company_filings": {
        "provider": "SEC EDGAR / CNInfo / exchange disclosures",
        "best_for": "competitor revenue, segment revenue, customer and geography exposure",
        "endpoint": "https://www.sec.gov/edgar/sec-api-documentation",
        "notes": "Use filings as primary evidence when market claims depend on listed companies.",
    },
}


class DataFetcher:
    def __init__(self, fred_api_key: Optional[str] = None):
        self.fred_api_key = fred_api_key or os.getenv("FRED_API_KEY")
        self._fred_client = None

    def check_available_sources(self) -> Dict[str, bool]:
        return {
            "direct_http": True,
            "fred": FRED_AVAILABLE and bool(self.fred_api_key),
            "worldbank_package": WBDATA_AVAILABLE,
            "akshare": AKSHARE_AVAILABLE,
            "yfinance": YFINANCE_AVAILABLE,
            "pytrends": PYTRENDS_AVAILABLE,
        }

    def get_source_catalog(self) -> Dict[str, Dict[str, str]]:
        return SOURCE_CATALOG.copy()

    def build_source_card(
        self,
        *,
        source_id: str,
        provider: str,
        dataset_or_title: str,
        metric: str,
        geography: str,
        period: str,
        unit: str,
        value_or_path: str,
        url_or_endpoint: str,
        transform_note: str,
        used_in: str,
        accessed_at: Optional[str] = None,
        last_updated_or_vintage: str = "",
    ) -> Dict[str, str]:
        return {
            "source_id": source_id,
            "provider": provider,
            "dataset_or_title": dataset_or_title,
            "metric": metric,
            "geography": geography,
            "period": period,
            "unit": unit,
            "value_or_path": value_or_path,
            "url_or_endpoint": url_or_endpoint,
            "accessed_at": accessed_at or datetime.now().strftime("%Y-%m-%d"),
            "last_updated_or_vintage": last_updated_or_vintage,
            "transform_note": transform_note,
            "used_in": used_in,
        }

    def get_worldbank_indicator_direct(
        self,
        country: str,
        indicator: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> pd.DataFrame:
        params = {"format": "json", "per_page": 20000}
        if start_year and end_year:
            params["date"] = f"{start_year}:{end_year}"
        url = (
            f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
            f"?{urlencode(params)}"
        )
        payload = _read_json(url)
        rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
        data = [
            {
                "date": item.get("date"),
                "value": item.get("value"),
                "country": item.get("country", {}).get("value"),
                "indicator": item.get("indicator", {}).get("id"),
                "source_url": url,
            }
            for item in rows
        ]
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values("date")
        return df

    def get_worldbank_indicator(
        self,
        country: str,
        indicator: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> pd.DataFrame:
        if WBDATA_AVAILABLE:
            date_range = None
            if start_year and end_year:
                date_range = (datetime(start_year, 1, 1), datetime(end_year, 12, 31))
            return wbdata.get_dataframe({indicator: "value"}, country=country, date=date_range)
        return self.get_worldbank_indicator_direct(country, indicator, start_year, end_year)

    def get_dbnomics_series(self, provider: str, dataset: str, series: str) -> pd.DataFrame:
        url = f"https://api.db.nomics.world/v22/series/{provider}/{dataset}/{series}"
        payload = _read_json(url)
        series_payload = payload.get("series", {}).get("docs", [])
        if not series_payload:
            return pd.DataFrame()
        doc = series_payload[0]
        values = doc.get("values", {})
        periods = doc.get("period", [])
        rows = [
            {
                "period": period,
                "value": values.get(str(idx)),
                "provider": provider,
                "dataset": dataset,
                "series": series,
                "source_url": url,
            }
            for idx, period in enumerate(periods)
        ]
        return pd.DataFrame(rows)

    def get_fred_series(self, series_id: str, start_date: Optional[str] = None) -> pd.Series:
        if not FRED_AVAILABLE:
            raise ImportError("Please install fredapi: pip install fredapi")
        if not self.fred_api_key:
            raise ValueError("FRED_API_KEY is required for fredapi.")
        if self._fred_client is None:
            self._fred_client = Fred(api_key=self.fred_api_key)
        return self._fred_client.get_series(series_id, observation_start=start_date)

    def get_china_gdp(self) -> pd.DataFrame:
        return self.call_akshare_function("macro_china_gdp")

    def get_china_cpi(self) -> pd.DataFrame:
        return self.call_akshare_function("macro_china_cpi")

    def get_china_pmi(self) -> pd.DataFrame:
        return self.call_akshare_function("macro_china_pmi")

    def search_akshare_functions(self, keyword: str) -> List[str]:
        if not AKSHARE_AVAILABLE:
            raise ImportError("Please install akshare: pip install akshare")
        return [
            name
            for name in dir(ak)
            if not name.startswith("_") and keyword.lower() in name.lower()
        ]

    def call_akshare_function(self, function_name: str, **kwargs: Any) -> pd.DataFrame:
        if not AKSHARE_AVAILABLE:
            raise ImportError("Please install akshare: pip install akshare")
        if function_name.startswith("_") or not hasattr(ak, function_name):
            raise ValueError(f"Unknown AkShare function: {function_name}")
        fn = getattr(ak, function_name)
        result = fn(**kwargs)
        if isinstance(result, pd.DataFrame):
            return result
        return pd.DataFrame(result)

    def get_china_industry_data(self, indicator: str) -> pd.DataFrame:
        raise ValueError(
            "Do not use get_china_industry_data as a generic shortcut. "
            "Search AkShare functions for the exact indicator, inspect the returned columns, "
            "then call call_akshare_function(function_name, **kwargs). "
            f"Requested indicator: {indicator}"
        )

    def get_company_financials(self, ticker: str) -> Dict[str, Any]:
        if not YFINANCE_AVAILABLE:
            raise ImportError("Please install yfinance: pip install yfinance")
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "ticker": ticker,
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "revenue": info.get("totalRevenue"),
            "profit_margin": info.get("profitMargins"),
            "source": "Yahoo Finance via yfinance; verify against company filings for final use.",
        }

    def get_company_history(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        if not YFINANCE_AVAILABLE:
            raise ImportError("Please install yfinance: pip install yfinance")
        return yf.Ticker(ticker).history(period=period)

    def get_search_trend(
        self,
        keyword: str,
        geo: str = "",
        timeframe: str = "today 12-m",
    ) -> pd.DataFrame:
        if not PYTRENDS_AVAILABLE:
            raise ImportError("Please install pytrends: pip install pytrends")
        pytrends = TrendReq(hl="zh-CN", tz=480)
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo)
        return pytrends.interest_over_time()

    def get_recent_window(self, days: int = 365) -> Dict[str, str]:
        end = datetime.now()
        start = end - timedelta(days=days)
        return {"start_date": start.strftime("%Y-%m-%d"), "end_date": end.strftime("%Y-%m-%d")}


def get_data_fetcher() -> DataFetcher:
    return DataFetcher()


def _read_json(url: str) -> Any:
    with urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    fetcher = DataFetcher()
    print(fetcher.check_available_sources())
    print(fetcher.get_source_catalog().keys())
