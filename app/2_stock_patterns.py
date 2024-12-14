import streamlit as st
from config import pagesetup as ps
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. Set Page Header
title = "FlowTrader"
subtitle = "Stock Patterns"
divider = True
ps.set_header(title=title, subtitle=subtitle, divider=divider)