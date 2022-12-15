import utils
import altair as alt
class Screening(utils.Technical):
    def __init__(self, stock, fromDate, now, Alpha, Beta):
        super().__init__(stock, fromDate, now, Alpha, Beta)
    def step_one(self):
        try:
            if (self.technical.loc[:, "DownMean"].iloc[-1] > self.technical.loc[:, "Close"].iloc[-1] and self.technical.loc[:, "BoxDownMean"].iloc[-1] > self.technical.loc[:, "Close"].iloc[-1]):
                return "Yes"
            else:
                return "No"
        except:
            return "Error"
