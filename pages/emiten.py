import streamlit as st
import yfinance as yf
import altair as alt
import utils
import datetime
import pandas as pd
st.set_page_config(
    page_title="Gxan",
    layout="wide"
)

oneYearAgo = datetime.datetime.now() - datetime.timedelta(days=2*365)
now = datetime.datetime.now()
kode, nama, file = utils.file()
stock_selectbox = st.selectbox(
    'Select Your Emiten?', kode)

chart = utils.Technical(stock_selectbox, oneYearAgo, now, utils.Alpha, utils.Beta).chart()
st.altair_chart(chart, use_container_width=True)

profile, financial, Techincal = st.tabs(["Profile", "Financial", "Techincal"])
ticker = utils.ticker(stock_selectbox) 

with profile:
    info = ticker.info
    st.subheader("Nama Perusahaan")
    st.write(info['longName'])
    st.subheader("Category")
    st.caption(info['sector'])
    st.subheader("Keterangan")
    st.write(info['longBusinessSummary'])
    st.subheader("Alamat")
    st.write(info['address1'], ", ", info['address2'], ", ",  info['city'], " - ", info['country'])
    
with financial: 
    fin = utils.Financial(ticker)
    st.caption("Total Pendapatan")
    st.altair_chart(fin.net_income(), use_container_width=True)

    st.caption("Arus Kas")
    st.altair_chart(fin.cash_flow(), use_container_width=True)

    st.caption("Neraca Keuangan")
    st.altair_chart(fin.balance_sheet(), use_container_width=True)

with Techincal:
    tech_ = utils.Technical(stock_selectbox, oneYearAgo, now, utils.Alpha, utils.Beta).analitic()
    st.write(tech_)