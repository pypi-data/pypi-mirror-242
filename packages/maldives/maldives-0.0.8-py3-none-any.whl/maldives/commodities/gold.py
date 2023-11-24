# TODO:
# - automate data gathering/generation
# - automate fitting
# - automate plotting
from wallstreet import Stock
from maldives.regression import LinearRegressor
from maldives.api import FredData

import pandas as pd
import numpy as np
import plotly.express as px


class GoldPriceModel(object):
    def __init__(self):
        self.df = None
        self.fitted = False
        self.current_price = np.nan
        self.model = None
        self.last_date = None

    def load_data(self, fred_api_key, num_months=60):
        # load gold futures prices
        gold = Stock('GC=F').historical(days_back=2500)
        gold['Date'] = pd.to_datetime(gold['Date'])
        gold['ClosingPrice'] = gold['Close']
        gold = gold.set_index('Date')[['ClosingPrice']]
        self.current_price = gold.ClosingPrice.values[-1]

        # load cpi and treasury yield
        fred = FredData(fred_api_key)
        cpi, treasury = fred.CPI(), fred.Treasury10Y()

        df = pd.merge_asof(cpi, gold.join(
            treasury), left_index=True, right_index=True, direction='nearest')
        df = df.dropna().tail(num_months)
        self.df = df
        self.last_date = self.df.index[-1].strftime('%Y-%m-%d')

    def fit(self):
        if self.df is None:
            raise ValueError(
                'No data available. Please call load_data() before calling fit().')
        self.model = LinearRegressor(transform=np.log, invtransform=np.exp)
        X, y = self.df[['CPI', 'Treasury10Y']], self.df['ClosingPrice']
        self.model.fit(X, y, shift=-1)

    def display(self, return_figures=False):
        if not self.fitted:
            self.fit()
        # calculate predictions
        X = self.df[['CPI', 'Treasury10Y']]
        pred, uncertainty = self.model.predict(X)

        # calculate probabilities
        diff = np.linspace(-350, 350, 101)
        price = pred[-1] + diff
        prob = uncertainty(diff)
        pvalue = uncertainty.integrate_box_1d(
            self.current_price-pred[-1], np.inf)

        # prob distribution
        fig1 = px.line(x=price, y=prob, title=f"R2={self.model.R2:.2f} p={pvalue:.4f} (last CPI: {self.last_date})") \
            .add_vline(self.current_price)
        fig1.update_layout(xaxis_title='Gold Price', yaxis_title='Probability', hovermode='x')

        # time series of predictions
        self.df['Prediction'] = pred
        self.df['Prediction'] = self.df.Prediction.shift(1)
        fig2 = px.line(self.df.dropna(), y=['Prediction', 'ClosingPrice'])
        fig2.update_layout(xaxis_title='Time', yaxis_title='Price', hovermode='x')
        if not return_figures:
            fig1.show(), fig2.show()
        else:
            return fig1, fig2
