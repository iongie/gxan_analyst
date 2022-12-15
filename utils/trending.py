import utils
import altair as alt

class Trending:
    def __init__(self, stock, fromDate, now, Alpha, Beta):
        df = utils.stock(stock, fromDate, now)
        self.dt_chart = df.copy()
        self.dt_chart['Down'] = self.dt_chart.loc[:, 'Close'].apply(lambda x : utils.checking_fibo(x, Alpha)[0])
        self.dt_chart['BoxDown'] = self.dt_chart.loc[:, 'Close'].apply(lambda x : utils.checking_fibo(x, Beta)[0])
        self.dt_chart["bbUp"] = utils.bollingerband(self.dt_chart.loc[:, 'Down'], 2, 20, 20)[0]
        self.dt_chart["bbDown"] = utils.bollingerband(self.dt_chart.loc[:, 'Down'], 2, 20, 20)[1]
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

        point = base.mark_circle(size=80).encode(
            alt.Y('Close')
        ).transform_filter(
            nearest
        )

        bollinger = alt.Chart(self.dt_chart).mark_bar(color="#FFE15D").encode(
            alt.X('Date',
                axis=alt.Axis(
                    format='%m/%d/%y',
                    labelAngle=-45,
                )
            ),
            alt.Y('bbUp'),
            alt.Y2('bbDown')
        )

        return(
            bollinger 
            + rule
            + bar
            + selectors
            + point
            ).properties(width=1200, height=400).interactive()