import streamlit as st
from config import pagesetup as ps

# 1. Set Page Config
st.set_page_config(page_title="FlowTrader", page_icon="assets/images/flowtrader_icon1.png", layout="wide", initial_sidebar_state="collapsed")

# 2. Set Page Header
ps.set_header(title="FlowTrader", subtitle="Home", divider=True)