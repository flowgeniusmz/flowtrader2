import streamlit as st

# 1. Config
#### 1A. Set Page Config
st.set_page_config(page_title="FlowTrader", page_icon="assets/images/flowtrader_main1_icon.jpg", layout="wide", initial_sidebar_state="collapsed")

#### 1B. Set Logo
image_path = "assets/images/flowtrader_main1.jpg"
icon_path = "assets/images/flowtrader_main1_icon.jpg"
logo = st.logo(image=image_path, size="large", icon_image=icon_path)

# 2. Pages
#### 2A. Set Individual pages
page_home = st.Page(page="app/home.py", title="Home", url_path="/welcome", default=True)
page_stock_data = st.Page(page="app/stock_data.py", title="Stock Data", url_path="/stockdata")
page_trade = st.Page(page="app/trade.py", title="Trade", url_path="/trade")

#### 2B. Set Page Lists
pages = [page_home, page_stock_data, page_trade]

# 3. Navigation
#### 3A. Set Navigation
nav = st.navigation(pages=pages)

#### 3B. Run Navigation
nav.run()

