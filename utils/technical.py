import utils
import altair as alt
import pandas as pd

class Technical:
    def __init__(self, stock, fromDate, now, Alpha, Beta):
        df = utils.stock(stock, fromDate, now)
        self.dt_chart = df.copy()
        self.dt_chart['Down'] = self.dt_chart.loc[:, 'Close'].apply(lambda x : utils.checking_fibo(x, Alpha)[0])
        self.dt_chart['BoxDown'] = self.dt_chart.loc[:, 'Close'].apply(lambda x : utils.checking_fibo(x, Beta)[0])
        self.dt_chart['Upper'] = self.dt_chart.loc[:, 'Close'].apply(lambda x : utils.checking_fibo(x, Alpha)[1])
        self.dt_chart['BoxUpper'] = self.dt_chart.loc[:, 'Close'].apply(lambda x : utils.checking_fibo(x, Beta)[1])

        self.technical = self.dt_chart.copy()
        self.technical['UpperMean'] =  self.technical.loc[:, 'Upper'].rolling(3).mean()
        self.technical['BoxUpperMean'] =   self.technical.loc[:, 'BoxUpper'].rolling(3).mean()
        self.technical['UpperMax'] =  self.technical.loc[:, 'UpperMean'].rolling(28).mean()
        self.technical['BoxUpperMax'] =   self.technical.loc[:, 'BoxUpperMean'].rolling(28).mean()     
        self.technical['DownMean'] = self.technical.loc[:, 'Down'].rolling(3).mean()
        self.technical['BoxDownMean'] = self.technical.loc[:, 'BoxDown'].rolling(3).mean()   
        self.technical['DownMin'] = self.technical.loc[:, 'DownMean'].rolling(28).mean()
        self.technical['BoxDownMin'] = self.technical.loc[:, 'BoxDownMean'].rolling(28).mean()

        self.Line = utils.Line(self.dt_chart.loc[:, "Close"].min(), self.dt_chart.loc[:, "Close"].max())

    def analitic(self):
        return self.technical.iloc[-1]

    def chart(self):
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Date'], empty='none')

        open_close_color = alt.condition("datum.Open <= datum.Close",
                                    alt.value("#38E54D"),
                                    alt.value("#FF6464"))

        base = alt.Chart(self.dt_chart).encode(
            alt.X('Date',
                axis=alt.Axis(
                    format='%m/%d/%y',
                    labelAngle=-45,
                    grid=False
                )
            ),
            color=open_close_color
        )

        selectors = base.mark_point().encode(
            x='Date',
            opacity=alt.value(0),
            tooltip = [
                alt.Tooltip('Date', format="%A, %d %b %Y", title="Date"),
                alt.Tooltip('Open', format=",", title="Open"),
                alt.Tooltip('Low', format=",", title="Low"),
                alt.Tooltip('High', format=",", title="High"),
                alt.Tooltip('Close', format=",", title="Close"),
            ]
        ).add_selection(
            nearest
        )

        rule = base.mark_rule().encode(
            alt.Y(
                    'Low',
                    title='Price',
                    scale=alt.Scale(zero=False),
                    axis=alt.Axis(grid=False)
                ),
            alt.Y2('High')
        )

        bar = base.mark_bar().encode(
            alt.Y('Open'),
            alt.Y2('Close')
        )

        down = alt.Chart(self.dt_chart).mark_line(color="#1DB9C3").encode(
            alt.X('Date',
                axis=alt.Axis(
                    format='%m/%d/%y',
                    labelAngle=-45,
                )
            ),
            alt.Y('Down')
        )

        boxdown = alt.Chart(self.dt_chart).mark_line(color="#7027A0").encode(
            alt.X('Date',
                axis=alt.Axis(
                    format='%m/%d/%y',
                    labelAngle=-45,
                )
            ),
            alt.Y('BoxDown')
        )

        rules = base.mark_rule(color='gray').encode(
            x='Date',
        ).transform_filter(
            nearest
        )

        point = base.mark_circle(size=80).encode(
            alt.Y('Close')
        ).transform_filter(
            nearest
        )

        downmean = alt.Chart(self.technical).mark_bar(color="#FFE15D").encode(
            alt.X('Date',
                axis=alt.Axis(
                    format='%m/%d/%y',
                    labelAngle=-45,
                )
            ),
            alt.Y('DownMean'),
            alt.Y2('BoxDownMean')
        )

        uppermean = alt.Chart(self.technical).mark_bar(color="#DC3535").encode(
            alt.X('Date',
                axis=alt.Axis(
                    format='%m/%d/%y',
                    labelAngle=-45,
                )
            ),
            alt.Y('UpperMean'),
            alt.Y2('BoxUpperMean')
        )


        downmin = alt.Chart(self.technical).mark_bar(color="#99FEFF").encode(
            alt.X('Date',
                axis=alt.Axis(
                    format='%m/%d/%y',
                    labelAngle=-45,
                )
            ),
            alt.Y('DownMin'),
            alt.Y2('BoxDownMin')
        )

        uppermax = alt.Chart(self.technical).mark_bar(color="#E3FCBF").encode(
            alt.X('Date',
                axis=alt.Axis(
                    format='%m/%d/%y',
                    labelAngle=-45,
                )
            ),
            alt.Y('UpperMax'),
            alt.Y2('BoxUpperMax')
        )

        lineAlpha = alt.Chart(pd.DataFrame({'y': self.Line[0]})).mark_rule(color='gray', strokeDash=[5,5]).encode(
            y='y'
        )

        lineBeta = alt.Chart(pd.DataFrame({'y': self.Line[1]})).mark_rule(color='gray', strokeDash=[1,1]).encode(
            y='y'
        )
        

        return(
            downmean
            + rules
            + lineAlpha
            + lineBeta
            + uppermean
            + uppermax
            + downmin
            + rule
            + bar
            + selectors
            + down
            + boxdown
            + point
            ).properties(width=1200, height=400).interactive()
    