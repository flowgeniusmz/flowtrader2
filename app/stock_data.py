import streamlit as st
from config import pagesetup as ps
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import time


# 1. Set Page Header
title = "FlowTrader"
subtitle = "Stock Data"
divider = True
ps.set_header(title=title, subtitle=subtitle, divider=divider)

# 2. Set Variables
intervals = ["1d", "1h"]
tickers0 = ["NVDA", "AAPL", "MSFT", "AMZN", "META", "GOOGL", "TSLA", "BRK.B", "GOOG", "AVGO", "JPM", "LLY", "UNH", "XOM", "V", "MA", "COST", "HD", "PG", "WMT", "JNJ", "NFLX", "CRM", "BAC", "ABBV", "ORCL", "CVX", "MRK", "WFC", "KO", "ADBE", "CSCO", "PEP", "ACN", "AMD", "LIN", "MCD", "NOW", "TMO", "ABT", "PM", "DIS", "INTU", "GE", "IBM", "ISRG", "TXN", "CAT", "GS", "QCOM", "MS", "HON", "NKE", "AMGN", "MDT", "LOW", "SPGI", "NEE", "BLK", "AMT", "SCHW", "RTX", "DHR", "LMT", "UNP", "INTC", "DE", "T", "USB", "C", "CVS", "MMM", "BA", "BKNG", "AXP", "DUK", "SO", "PLD", "CI", "MO", "PFE", "MDLZ", "TGT", "SYK", "COP", "MMC", "ELV", "CB", "ADP", "GILD", "BDX", "ADI", "PNC", "TJX", "APD", "ICE", "ITW", "EOG", "CL", "PSA", "NSC", "EW", "AON", "VRTX", "CME", "FISV", "HUM", "AEP", "GM", "MCO", "SHW", "ETN", "F", "BSX", "WM", "REGN", "D", "MPC", "MET", "KMB", "EMR", "DG", "SBUX", "KLAC", "ORLY", "FDX", "AIG", "TRV", "EXC", "LRCX", "ADM", "COF", "ECL", "CTAS", "MSI", "ROP", "MAR", "SPG", "TEL", "OXY", "AFL", "WBA", "PRU", "MNST", "PSX", "WELL", "SLB", "ROST", "KHC", "CNC", "DLR", "CTSH", "BK", "ALL", "SRE", "MCK", "WMB", "HLT", "RSG", "STZ", "NOC", "IDXX", "JCI", "PGR", "AZO", "BIIB", "CDNS", "PAYX", "XEL", "ED", "PCAR", "APH", "DOW", "ODFL", "CMG", "WEC", "TT", "EQR", "ES", "AWK", "VLO", "PPG", "CARR", "KMI", "FTNT", "AMP", "DLTR", "HSY", "SYY", "MTD", "SNPS", "ANET", "FAST", "GPN", "HCA", "AME", "BAX", "MCHP", "PEG", "WAT", "OTIS", "VRSK", "DFS", "GLW", "ARE", "VICI", "ZTS", "NEM", "DHI", "KEYS", "MLM", "LEN", "FIS", "WBD", "KDP", "APTV", "LUV", "SWK", "NUE", "URI", "FITB", "HBAN", "CDW", "ETR", "CAG", "HIG", "PPL", "VTR", "RMD", "CMS", "AEE", "LHX", "TSCO", "EPAM", "WAB", "EFX", "VMC", "CINF", "DTE", "EIX", "LVS", "ZBH", "XYL", "CHD", "STE", "MPWR", "EXPE", "NTRS", "RJF", "CNP", "ATO", "ESS", "AVB", "UDR", "MAA", "PEAK", "IRM", "BXP", "SLG", "HST", "FRT", "KIM", "REG"]
tickers1 = ["AAPL", "ABBV", "ABT", "ACN", "ADBE", "ADI", "ADM", "ADP", "AEE", "AEP", "AFL", "AIG", "ALL", "AMD", "AME", "AMGN", "AMP", "AMT", "AMZN", "ANET", "AON", "APD", "APH", "APTV", "ARE", "ATO", "AVB", "AVGO", "AWK", "AXP", "AZO", "BA", "BAC", "BAX", "BDX", "BIIB", "BK", "BKNG", "BLK", "BRK.B", "BSX", "BXP", "C", "CAG", "CARR", "CAT", "CB", "CDNS", "CDW", "CHD", "CI", "CINF", "CL", "CME", "CMG", "CMS", "CNC", "CNP", "COF", "COP", "COST", "CRM", "CSCO", "CTAS", "CTSH", "CVS", "CVX", "D", "DE", "DFS", "DG", "DHI", "DHR", "DIS", "DLR", "DLTR", "DOW", "DTE", "DUK", "ECL", "ED", "EFX", "EIX", "ELV", "EMR", "EOG", "EPAM", "EQR", "ES", "ESS", "ETN", "ETR", "EW", "EXC", "EXPE", "F", "FAST", "FDX", "FIS", "FISV", "FITB", "FRT", "FTNT", "GE", "GILD", "GLW", "GM", "GOOG", "GOOGL", "GPN", "GS", "HBAN", "HCA", "HD", "HIG", "HLT", "HON", "HST", "HSY", "HUM", "IBM", "ICE", "IDXX", "INTC", "INTU", "IRM", "ISRG", "ITW", "JCI", "JNJ", "JPM", "KDP", "KEYS", "KHC", "KIM", "KLAC", "KMB", "KMI", "KO", "LEN", "LHX", "LIN", "LLY", "LMT", "LOW", "LRCX", "LUV", "LVS", "MA", "MAA", "MAR", "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "META", "MLM", "MMC", "MMM", "MNST", "MO", "MPC", "MPWR", "MRK", "MS", "MSFT", "MSI", "MTD", "NEE", "NEM", "NFLX", "NKE", "NOC", "NOW", "NSC", "NTRS", "NUE", "NVDA", "ODFL", "ORCL", "ORLY", "OTIS", "OXY", "PAYX", "PCAR", "PEAK", "PEG", "PEP", "PFE", "PG", "PGR", "PLD", "PM", "PNC", "PPG", "PPL", "PRU", "PSA", "PSX", "QCOM", "REG", "REGN", "RJF", "RMD", "ROP", "ROST", "RSG", "RTX", "SBUX", "SCHW", "SHW", "SLB", "SLG", "SNPS", "SO", "SPG", "SPGI", "SRE", "STE", "STZ", "SWK", "SYK", "SYY", "T", "TEL", "TGT", "TJX", "TMO", "TRV", "TSCO", "TSLA", "TT", "TXN", "UDR", "UNH", "UNP", "URI", "USB", "V", "VICI", "VLO", "VMC", "VRSK", "VRTX", "VTR", "WAB", "WAT", "WBA", "WBD", "WEC", "WELL", "WFC", "WM", "WMB", "WMT", "XEL", "XOM", "XYL", "ZBH", "ZTS"]
end_date = datetime.today()
start_date_1d = end_date - timedelta(days=120)
start_date_1h = end_date - timedelta(days=60)

# 3. Display
#### 3A. Stock Selector
st.header("Select a stock")
ticker_selection = st.selectbox(label="Stock Ticker", options=tickers1, index=0, key="selected_ticker")
if ticker_selection:
    st.markdown(f"Selected {ticker_selection}")
