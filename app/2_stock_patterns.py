## REF: https://colab.research.google.com/drive/1BBaltwtqv-KFYXbUIz8ipJ06iqVJTPYG?usp=sharing#scrollTo=OJSkZ24pEuIg
## REF: https://medium.com/@wl8380/decoding-the-market-how-i-built-a-stock-pattern-detective-in-python-2fc106686a51

import streamlit as st
from config import pagesetup as ps
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 0. Set Page Header
title = "FlowTrader"
subtitle = "Stock Patterns"
divider = True
ps.set_header(title=title, subtitle=subtitle, divider=divider)

# 1. Set Variables
available_tickers = ["AAPL", "ABBV", "ABT", "ACN", "ADBE", "ADI", "ADM", "ADP", "AEE", "AEP", "AFL", "AIG", "ALL", "AMD", "AME", "AMGN", "AMP", "AMT", "AMZN", "ANET", "AON", "APD", "APH", "APTV", "ARE", "ATO", "AVB", "AVGO", "AWK", "AXP", "AZO", "BA", "BAC", "BAX", "BDX", "BIIB", "BK", "BKNG", "BLK", "BRK.B", "BSX", "BXP", "C", "CAG", "CARR", "CAT", "CB", "CDNS", "CDW", "CHD", "CI", "CINF", "CL", "CME", "CMG", "CMS", "CNC", "CNP", "COF", "COP", "COST", "CRM", "CSCO", "CTAS", "CTSH", "CVS", "CVX", "D", "DE", "DFS", "DG", "DHI", "DHR", "DIS", "DLR", "DLTR", "DOW", "DTE", "DUK", "ECL", "ED", "EFX", "EIX", "ELV", "EMR", "EOG", "EPAM", "EQR", "ES", "ESS", "ETN", "ETR", "EW", "EXC", "EXPE", "F", "FAST", "FDX", "FIS", "FISV", "FITB", "FRT", "FTNT", "GE", "GILD", "GLW", "GM", "GOOG", "GOOGL", "GPN", "GS", "HBAN", "HCA", "HD", "HIG", "HLT", "HON", "HST", "HSY", "HUM", "IBM", "ICE", "IDXX", "INTC", "INTU", "IRM", "ISRG", "ITW", "JCI", "JNJ", "JPM", "KDP", "KEYS", "KHC", "KIM", "KLAC", "KMB", "KMI", "KO", "LEN", "LHX", "LIN", "LLY", "LMT", "LOW", "LRCX", "LUV", "LVS", "MA", "MAA", "MAR", "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "META", "MLM", "MMC", "MMM", "MNST", "MO", "MPC", "MPWR", "MRK", "MS", "MSFT", "MSI", "MTD", "NEE", "NEM", "NFLX", "NKE", "NOC", "NOW", "NSC", "NTRS", "NUE", "NVDA", "ODFL", "ORCL", "ORLY", "OTIS", "OXY", "PAYX", "PCAR", "PEAK", "PEG", "PEP", "PFE", "PG", "PGR", "PLD", "PM", "PNC", "PPG", "PPL", "PRU", "PSA", "PSX", "QCOM", "REG", "REGN", "RJF", "RMD", "ROP", "ROST", "RSG", "RTX", "SBUX", "SCHW", "SHW", "SLB", "SLG", "SNPS", "SO", "SPG", "SPGI", "SRE", "STE", "STZ", "SWK", "SYK", "SYY", "T", "TEL", "TGT", "TJX", "TMO", "TRV", "TSCO", "TSLA", "TT", "TXN", "UDR", "UNH", "UNP", "URI", "USB", "V", "VICI", "VLO", "VMC", "VRSK", "VRTX", "VTR", "WAB", "WAT", "WBA", "WBD", "WEC", "WELL", "WFC", "WM", "WMB", "WMT", "XEL", "XOM", "XYL", "ZBH", "ZTS"]
end_date = datetime.today()
start_date_1d = end_date - timedelta(days=120)
start_date_1h = end_date - timedelta(days=60)

# 2. Functions
#### 2A. Data Fetching and Cleaning
def get_clean_financial_data(ticker: str, start_date: str, end_date: str):
    data = yf.download(tickers=ticker, start=start_date, end=end_date)

    # Clean Structure
    data.columns = data.columns.get_level_values(level=0)

    # Handle missing values
    data = data.ffill()

    # Standardize timezone
    data.index = data.index.tz_localize(None)

    return data

#### 2B. Pattern Recogniition Function
def identify_candlestick_patterns(data):
    patterns = []
    
    for i in range(1, len(data)):
        open_price = data['Open'].iloc[i]
        close_price = data['Close'].iloc[i]
        prev_open = data['Open'].iloc[i - 1]
        prev_close = data['Close'].iloc[i - 1]

        if close_price > open_price and prev_close < prev_open and close_price > prev_open and open_price < prev_close:
            patterns.append('Bullish Engulfing')

        elif close_price < open_price and prev_close > prev_open and close_price < prev_open and open_price > prev_close:
            patterns.append('Bearish Engulfing')

        elif abs(close_price - open_price) <= (0.01 * open_price):
            patterns.append('Doji')

        elif (close_price > open_price and (open_price - data['Low'].iloc[i]) > 2 * (close_price - open_price)):
            patterns.append('Hammer')

        elif (close_price < open_price and (data['High'].iloc[i] - open_price) > 2 * (open_price - close_price)):
            patterns.append('Shooting Star')

        else:
            patterns.append('No Pattern')

    # Add an empty value for the first entry
    patterns.insert(0, 'No Pattern')

    return patterns

# Display
selected_ticker = st.selectbox(label="Select Ticker", options=available_tickers, index=0, key="ticker_selected", placeholder="Select a ticker")
selected_start_date = st.date_input(label="Select Start Date", key="start_date_selected", format="YYYY-MM-DD")
selected_end_date = st.date_input(label="Select End Date", key="end_date_selected", format="YYYY-MM-DD")
submit = st.button(label="Submit", key="user_input_submitted")
if submit:
    if selected_ticker and selected_start_date and selected_end_date:
        st.toast("Getting data please wait...⏳")
        # Step 5: Fetch and clean Google stock data
        data = get_clean_financial_data(ticker=selected_ticker, start_date=selected_start_date, end_date=selected_end_date)

        # Step 6: Identify candlestick patterns
        data['Pattern'] = identify_candlestick_patterns(data=data)

        # Step 7: Create a candlestick chart
        fig = go.Figure()

        # Step 8: Add candlestick trace
        fig.add_trace(go.Candlestick(x=data.index,open=data['Open'],high=data['High'],low=data['Low'],close=data['Close'],name='Candlesticks')) 

        # Step 9: Add traces for different patterns
        colors = {'Bullish Engulfing': 'green','Bearish Engulfing': 'red','Doji': 'gray','Hammer': 'blue','Shooting Star': 'purple',}

        for pattern in colors.keys():
            pattern_data = data[data['Pattern'] == pattern]
            if not pattern_data.empty:
                fig.add_trace(go.Scatter(x=pattern_data.index,y=pattern_data['High'],mode='markers',marker=dict(color=colors[pattern], size=10),name=pattern,showlegend=True))
                
        # Step 10: Update layout
        fig.update_layout(title='META Candlestick Chart with Patterns',xaxis_title='Date',yaxis_title='Stock Price (USD)',xaxis_rangeslider_visible=False)

        # Step 11: Show the figure
        st.plotly_chart(fig, use_container_width=True)
