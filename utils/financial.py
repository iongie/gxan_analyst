import streamlit as st
import altair as alt
class Financial:
    def __init__(self, Ticker):
        self.ni = Ticker.financials.loc["Total Revenue"].rename_axis('Date').reset_index()
        self.cf = Ticker.cashflow.transpose().rename_axis('Date').reset_index()
        self.bs = Ticker.balancesheet.transpose().rename_axis('Date').reset_index()
    
    def net_income(self):
        return alt.Chart(self.ni).mark_bar(size=50).encode(
            alt.X('Date', axis=alt.Axis(tickCount="year", grid=False)),
            alt.Y('Total Revenue', axis=alt.Axis(grid=False, labelExpr='datum.value / 1E9 + "B"')),
            tooltip=[
                alt.Tooltip('Total Revenue', format="~s", title="Revenue")
                ]
        ).properties(width="container",height=300).interactive()
    
    def balance_sheet(self):
        return alt.Chart(self.bs).transform_fold(
        ['Total Current Assets', 'Total Current Liabilities'], as_=["category", "value"]).mark_bar(size=50).encode(
            alt.X('Date', axis=alt.Axis(tickCount="year", grid=False)),
            alt.Y('value:Q', axis=alt.Axis(grid=False, title=None, labelExpr='datum.value / 1E9 + "B"')), 
            color=alt.Color('category:N', legend=alt.Legend(orient="bottom", direction="horizontal", labelFontSize=10, labelLimit=0)),
            tooltip=[
                alt.Tooltip('Total Current Assets', format="~s", title="Assets"),
                alt.Tooltip('Total Current Liabilities', format="~s", title="Liabilities"),
                ]
        ).properties(width="container",height=300).interactive()

    def cash_flow(self):
        return alt.Chart(self.cf).transform_fold(
        ['Total Cashflows From Investing Activities', 'Total Cash From Financing Activities', 'Total Cash From Operating Activities'], as_=["category", "value"]).mark_bar(size=50).encode(
            alt.X('Date', axis=alt.Axis(tickCount="year", grid=False)),
            alt.Y('value:Q', axis=alt.Axis(grid=False, title=None, labelExpr='datum.value / 1E9 + "B"')), 
            color=alt.Color('category:N', legend=alt.Legend(orient="bottom", direction="horizontal", labelFontSize=10, labelLimit=0)),
            tooltip=[
                alt.Tooltip('Total Cashflows From Investing Activities', format="~s", title="Investing"),
                alt.Tooltip('Total Cash From Financing Activities', format="~s", title="Financing"),
                alt.Tooltip('Total Cash From Operating Activities', format="~s", title="Operating")
                ]
        ).properties(width="container",height=300).interactive()