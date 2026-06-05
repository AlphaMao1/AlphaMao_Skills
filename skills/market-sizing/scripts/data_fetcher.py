"""
Market Sizing Data Fetcher
==========================

统一的数据获取接口，封装多个免费数据源：
- FRED: 美国宏观经济数据
- World Bank: 跨国宏观数据
- AkShare: 中国金融+宏观数据 (最全面)
- Baostock: 中国 A 股历史数据
- yfinance: 全球上市公司财务
- pytrends: Google 搜索趋势

使用方法:
    from data_fetcher import DataFetcher
    df = DataFetcher()
    gdp = df.get_china_gdp()
"""

import os
from typing import Optional, Union
from datetime import datetime, timedelta
import warnings

# 尝试导入各个数据源库
try:
    import pandas as pd
except ImportError:
    raise ImportError("请安装 pandas: pip install pandas")

# 可选依赖
FRED_AVAILABLE = False
WBDATA_AVAILABLE = False
AKSHARE_AVAILABLE = False
BAOSTOCK_AVAILABLE = False
YFINANCE_AVAILABLE = False
PYTRENDS_AVAILABLE = False

try:
    from fredapi import Fred
    FRED_AVAILABLE = True
except ImportError:
    pass

try:
    import wbdata
    WBDATA_AVAILABLE = True
except ImportError:
    pass

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    pass

try:
    import baostock as bs
    BAOSTOCK_AVAILABLE = True
except ImportError:
    pass

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    pass

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except ImportError:
    pass


class DataFetcher:
    """
    统一数据获取接口
    
    Example:
        >>> df = DataFetcher()
        >>> df.check_available_sources()
        {'fred': True, 'worldbank': True, 'akshare': True, ...}
        
        >>> gdp = df.get_china_gdp()
        >>> print(gdp.tail())
    """
    
    def __init__(self, fred_api_key: Optional[str] = None):
        """
        初始化数据获取器
        
        Args:
            fred_api_key: FRED API Key (可从环境变量 FRED_API_KEY 读取)
        """
        self.fred_api_key = fred_api_key or os.getenv("FRED_API_KEY")
        self._fred_client = None
        self._baostock_logged_in = False
        
    def check_available_sources(self) -> dict:
        """检查哪些数据源可用"""
        return {
            "fred": FRED_AVAILABLE and self.fred_api_key is not None,
            "worldbank": WBDATA_AVAILABLE,
            "akshare": AKSHARE_AVAILABLE,
            "baostock": BAOSTOCK_AVAILABLE,
            "yfinance": YFINANCE_AVAILABLE,
            "pytrends": PYTRENDS_AVAILABLE,
        }
    
    # ==================== FRED (美国宏观) ====================
    
    def get_fred_series(self, series_id: str, start_date: Optional[str] = None) -> pd.Series:
        """
        获取 FRED 数据序列
        
        Args:
            series_id: FRED 序列 ID (如 "FEDFUNDS", "GDP", "CPIAUCSL")
            start_date: 起始日期 (YYYY-MM-DD)
            
        常用序列:
            - GDP: 美国 GDP
            - FEDFUNDS: 联邦基金利率
            - CPIAUCSL: CPI 指数
            - UNRATE: 失业率
            - M2SL: M2 货币供应量
        """
        if not FRED_AVAILABLE:
            raise ImportError("请安装 fredapi: pip install fredapi")
        if not self.fred_api_key:
            raise ValueError("需要 FRED API Key，请设置环境变量 FRED_API_KEY")
        
        if self._fred_client is None:
            self._fred_client = Fred(api_key=self.fred_api_key)
        
        return self._fred_client.get_series(series_id, observation_start=start_date)
    
    # ==================== World Bank (跨国宏观) ====================
    
    def get_worldbank_indicator(
        self, 
        country: str, 
        indicator: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> pd.DataFrame:
        """
        获取世界银行指标数据
        
        Args:
            country: 国家代码 (如 "CN", "US", "JP")
            indicator: 指标代码
            start_year: 起始年份
            end_year: 结束年份
            
        常用指标:
            - NY.GDP.MKTP.CD: GDP (当前美元)
            - NY.GDP.PCAP.CD: 人均 GDP
            - SP.POP.TOTL: 总人口
            - NE.EXP.GNFS.ZS: 出口占 GDP 比例
            - FP.CPI.TOTL.ZG: 通胀率 (CPI)
        """
        if not WBDATA_AVAILABLE:
            raise ImportError("请安装 wbdata: pip install wbdata")
        
        date_range = None
        if start_year and end_year:
            date_range = (datetime(start_year, 1, 1), datetime(end_year, 12, 31))
        
        data = wbdata.get_dataframe({indicator: "value"}, country=country, date=date_range)
        return data
    
    # ==================== AkShare (中国宏观) ====================
    
    def get_china_gdp(self) -> pd.DataFrame:
        """获取中国 GDP 季度数据"""
        if not AKSHARE_AVAILABLE:
            raise ImportError("请安装 akshare: pip install akshare")
        return ak.macro_china_gdp()
    
    def get_china_cpi(self) -> pd.DataFrame:
        """获取中国 CPI 月度数据"""
        if not AKSHARE_AVAILABLE:
            raise ImportError("请安装 akshare: pip install akshare")
        return ak.macro_china_cpi()
    
    def get_china_pmi(self) -> pd.DataFrame:
        """获取中国 PMI 数据"""
        if not AKSHARE_AVAILABLE:
            raise ImportError("请安装 akshare: pip install akshare")
        return ak.macro_china_pmi()
    
    def get_china_money_supply(self) -> pd.DataFrame:
        """获取中国货币供应量 (M0, M1, M2)"""
        if not AKSHARE_AVAILABLE:
            raise ImportError("请安装 akshare: pip install akshare")
        return ak.macro_china_supply_of_money()
    
    def get_china_industry_data(self, indicator: str) -> pd.DataFrame:
        """
        获取中国行业产量数据
        
        Args:
            indicator: 可用值包括 "发电量", "汽车产量", "钢材产量" 等
        """
        if not AKSHARE_AVAILABLE:
            raise ImportError("请安装 akshare: pip install akshare")
        
        # AkShare 的行业数据接口
        try:
            return ak.macro_china_market_margin_sz()  # 示例，实际需要根据 indicator 选择
        except Exception as e:
            warnings.warn(f"获取行业数据失败: {e}")
            return pd.DataFrame()
    
    def search_akshare_functions(self, keyword: str) -> list:
        """
        搜索 AkShare 可用函数
        
        Args:
            keyword: 搜索关键词 (如 "gdp", "cpi", "汽车")
        """
        if not AKSHARE_AVAILABLE:
            raise ImportError("请安装 akshare: pip install akshare")
        
        all_funcs = [f for f in dir(ak) if not f.startswith("_")]
        return [f for f in all_funcs if keyword.lower() in f.lower()]
    
    # ==================== Baostock (A 股数据) ====================
    
    def _ensure_baostock_login(self):
        """确保 Baostock 已登录"""
        if not self._baostock_logged_in:
            bs.login()
            self._baostock_logged_in = True
    
    def get_a_share_financials(self, stock_code: str, year: int = None) -> pd.DataFrame:
        """
        获取 A 股财务数据
        
        Args:
            stock_code: 股票代码 (如 "sh.600000", "sz.000001")
            year: 年份
        """
        if not BAOSTOCK_AVAILABLE:
            raise ImportError("请安装 baostock: pip install baostock")
        
        self._ensure_baostock_login()
        
        if year is None:
            year = datetime.now().year - 1
        
        rs = bs.query_profit_data(code=stock_code, year=year, quarter=4)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        return pd.DataFrame(data_list, columns=rs.fields)
    
    def get_a_share_history(
        self, 
        stock_code: str, 
        start_date: str = None, 
        end_date: str = None,
        frequency: str = "d"
    ) -> pd.DataFrame:
        """
        获取 A 股历史行情
        
        Args:
            stock_code: 股票代码
            start_date: 起始日期 (YYYY-MM-DD)
            end_date: 结束日期
            frequency: 频率 (d=日, w=周, m=月)
        """
        if not BAOSTOCK_AVAILABLE:
            raise ImportError("请安装 baostock: pip install baostock")
        
        self._ensure_baostock_login()
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        rs = bs.query_history_k_data_plus(
            stock_code,
            "date,code,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=end_date,
            frequency=frequency
        )
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        return pd.DataFrame(data_list, columns=rs.fields)
    
    # ==================== yfinance (全球上市公司) ====================
    
    def get_company_financials(self, ticker: str) -> dict:
        """
        获取上市公司财务数据
        
        Args:
            ticker: 股票代码 (如 "AAPL", "MSFT", "LMT")
            
        Returns:
            dict: 包含 revenue, net_income, market_cap 等
        """
        if not YFINANCE_AVAILABLE:
            raise ImportError("请安装 yfinance: pip install yfinance")
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "ticker": ticker,
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "revenue": info.get("totalRevenue"),
            "net_income": info.get("netIncomeToCommon"),
            "profit_margin": info.get("profitMargins"),
            "pe_ratio": info.get("trailingPE"),
            "ps_ratio": info.get("priceToSalesTrailing12Months"),
        }
    
    def get_company_history(
        self, 
        ticker: str, 
        period: str = "1y"
    ) -> pd.DataFrame:
        """
        获取股价历史
        
        Args:
            ticker: 股票代码
            period: 时间范围 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
        """
        if not YFINANCE_AVAILABLE:
            raise ImportError("请安装 yfinance: pip install yfinance")
        
        stock = yf.Ticker(ticker)
        return stock.history(period=period)
    
    # ==================== pytrends (搜索趋势) ====================
    
    def get_search_trend(
        self, 
        keyword: str, 
        geo: str = "", 
        timeframe: str = "today 12-m"
    ) -> pd.DataFrame:
        """
        获取 Google 搜索趋势
        
        Args:
            keyword: 搜索关键词
            geo: 地区代码 (如 "CN", "US", "" 表示全球)
            timeframe: 时间范围 (如 "today 12-m", "today 3-m", "2020-01-01 2024-01-01")
        """
        if not PYTRENDS_AVAILABLE:
            raise ImportError("请安装 pytrends: pip install pytrends")
        
        pytrends = TrendReq(hl='zh-CN', tz=480)
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo)
        return pytrends.interest_over_time()
    
    def compare_search_trends(
        self, 
        keywords: list, 
        geo: str = "", 
        timeframe: str = "today 12-m"
    ) -> pd.DataFrame:
        """
        比较多个关键词的搜索趋势
        
        Args:
            keywords: 关键词列表 (最多 5 个)
            geo: 地区代码
            timeframe: 时间范围
        """
        if not PYTRENDS_AVAILABLE:
            raise ImportError("请安装 pytrends: pip install pytrends")
        
        if len(keywords) > 5:
            keywords = keywords[:5]
            warnings.warn("Google Trends 最多支持 5 个关键词，已截断")
        
        pytrends = TrendReq(hl='zh-CN', tz=480)
        pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo=geo)
        return pytrends.interest_over_time()
    
    # ==================== 清理 ====================
    
    def close(self):
        """清理资源"""
        if self._baostock_logged_in:
            bs.logout()
            self._baostock_logged_in = False


# 快捷函数
def get_data_fetcher() -> DataFetcher:
    """获取 DataFetcher 单例"""
    return DataFetcher()


if __name__ == "__main__":
    # 测试可用数据源
    df = DataFetcher()
    print("可用数据源:", df.check_available_sources())
    
    # 测试 AkShare (中国数据)
    if AKSHARE_AVAILABLE:
        print("\n中国 GDP 数据:")
        print(df.get_china_gdp().head())
