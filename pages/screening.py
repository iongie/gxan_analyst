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
categories = st.selectbox(
    'Select Your Favourite Categories?', ("ALL", "SYARIAH", "NON SYARIAH"))
index = st.selectbox(
    'Select Your Favourite Index?', ("LQ45", "IDX80", "MNC36", "PEFINDO25", "KOMPAS100", "SMINFRA18", "NOINDEX"))
if (categories == "ALL"):    
    emiten = file.loc[file[index].eq(1), ["Kode", "Nama Perusahaan", "Tanggal Pencatatan", "Shares"]].copy()
    emiten["ParamOne"] = emiten.loc[:, "Kode"].apply(lambda x: utils.Screening(x, oneYearAgo, now, utils.Alpha, utils.Beta).step_one())
    st.write(emiten)
elif (categories == "NON SYARIAH"):
    emiten = file.loc[file[index].eq(1) &
                       file['Syariah'].eq(0), ["Kode", "Nama Perusahaan", "Tanggal Pencatatan", "Shares"]].copy()
    emiten["ParamOne"] = emiten.loc[:, "Kode"].apply(lambda x: utils.Screening(x, oneYearAgo, now, utils.Alpha, utils.Beta).step_one())
    st.write(emiten)
else:
    emiten = file.loc[file[index].eq(1) &
                       file['Syariah'].eq(1), ["Kode", "Nama Perusahaan", "Tanggal Pencatatan", "Shares"]].copy()
    emiten["ParamOne"] = emiten.loc[:, "Kode"].apply(lambda x: utils.Screening(x, oneYearAgo, now, utils.Alpha, utils.Beta).step_one())
    st.write(emiten)
