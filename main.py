import streamlit as st
from datetime import date
import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

st.set_page_config(page_title='Stock Analyzer Dashboard', layout='wide')
bg_color = '#0E1117'
text_color = '#FFFFFF'

st.markdown("<h1 style='color:white; font-size:32px;'>Stock Analyzer Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:white;'>Welcome to the Stock Analyzer Dashboard! This dashboard allows you to analyze stock data by reviewing the historical data and parameters like 30 day rolling average. Go from raw data to meaningful dashboard to support your decisions on the market!</p>", unsafe_allow_html=True)

stock_ticker = st.text_input('Enter Stock Ticker Symbol', 'AAPL')
if stock_ticker == '':
    st.info('Please enter a valid stock ticker symbol.')
else:
    start_date = st.date_input('Select Start Date', value=date.today())
    end_date = st.date_input('Select End Date', value=date.today())
    
    df = yf.download(stock_ticker, start=start_date, end=end_date)
    
    if df.empty:
        st.info('No data available for the selected ticker or date range.')
    else:
        df.columns = df.columns.droplevel(1) if hasattr(df.columns, 'levels') else df.columns
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Day_of_week'] = df['Date'].dt.day_name()
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['Day'] = df['Date'].dt.day
        df['Daily_Return'] = df['Close'].pct_change()
        df['SMA_30'] = df['Close'].rolling(window=30).mean()
        df['Trend'] = np.where(df['Close'] > df['SMA_30'], 'Uptrend', 'Downtrend')
        
        st.write('Data :')
        st.dataframe(df, use_container_width=True)

        # ---- Closing Price vs SMA ----
        st.markdown("<h5 style='color:white;'>Closing Price vs SMA_30</h5>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(df['Date'], df['Close'], label='Close', color='#22D3EE', linewidth=1.6)
        ax.plot(df['Date'], df['SMA_30'], label='SMA_30', color='#A78BFA', linewidth=1.4)
        ax.set_facecolor(bg_color)
        fig.patch.set_facecolor(bg_color)
        ax.tick_params(colors='#9CA3AF', labelsize=8)
        for spine in ax.spines.values():
            spine.set_visible(False)
        st.pyplot(fig)

        # ---- Trading Volume ----
        st.markdown("<h5 style='color:white;'>Trading Volume</h5>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8,2.6))
        ax.bar(df['Date'], df['Volume'], color='#38BDF8', width=1.0)
        ax.set_facecolor(bg_color)
        fig.patch.set_facecolor(bg_color)
        ax.tick_params(colors='#9CA3AF', labelsize=8)
        for spine in ax.spines.values():
            spine.set_visible(False)
        st.pyplot(fig)

        # ---- Daily Return Distribution ----
        st.markdown("<h5 style='color:white;'>Daily Return Distribution</h5>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 2.6))
        ax.hist(df['Daily_Return'].dropna(), bins=40, color='#818CF8')
        ax.set_facecolor(bg_color)
        fig.patch.set_facecolor(bg_color)
        ax.tick_params(colors='#9CA3AF', labelsize=8)
        for spine in ax.spines.values():
            spine.set_visible(False)
        st.pyplot(fig)

        # ---- Trend Summary (Pie Chart) ----
        st.markdown("<h5 style='color:white;'>Trend Summary</h5>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        trend_counts = df['Trend'].value_counts()
        ax.pie(
            trend_counts.values,
            labels=trend_counts.index,
            autopct='%1.0f%%',
            colors=['orchid', 'teal'],
            textprops={'color': text_color, 'fontsize': 9}
        )
        fig.patch.set_facecolor(bg_color)
        st.pyplot(fig)