import streamlit as st
import pandas as pd
import yfinance as yf

def file():
    file = pd.read_excel('./file/Daftar Saham.xlsx')
    kode = tuple(file.loc[:, 'Kode'].to_list())
    nama = tuple(file.loc[:, 'Nama Perusahaan'].to_list())
    return (kode, nama, file)

def ticker(kode):
    stock = yf.Ticker(kode+".JK")
    return stock

def stock(kode, start, end):
    return yf.download(kode+".JK", start=start, end=end).reset_index().sort_index(ascending=True)
