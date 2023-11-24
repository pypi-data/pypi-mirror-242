import pandas as pd

from ..strategy import Strategy
from ...core import History, Side


class RsiStrategy(Strategy):
    """
    A strategy that generates buy/sell signals based on the RSI indicator.

    Parameters:
    - period (int): Number of days to roll the RSI window.
    - upper_bound (int): the upper threshold to start selling
    - lower_bound (int): the lower threshold to start buying

    Methods:
    - fit(history): Calculate moving averages and identify trends.
    - execute(row, idx, history) -> dict: Generate trading signals based on moving averages.
    """

    def __init__(self, window=14, upper_bound=70, lower_bound=30):
        super().__init__()
        self.window = window
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    def fit(self, history):
        """
        Calculate moving averages and identify trends.

        Args:
        - history (History): Historical price data of multiple equities.

        Returns:
        None
        """
        pass

    def execute(self, idx: pd.Index, position: pd.Series, history: History) -> pd.Series:
        """
        Generate trading signals based on Relative Strength Index(RSI).

        Args:
        - row (pd.Series): Latest row of equity prices.
        - idx (int): Index of the current row.
        - history (pd.DataFrame): Historical price data of multiple equities.

        Returns:
        dict: Trading signals for each equity.
        """
        signals = pd.Series(TradeSignal(TransactionType.WAIT), index=history.securities.values())
        loc = history.df.index.get_loc(idx)

        if loc > self.window:
            rsi = history.indicators.technical.rsi(window=self.window).loc[idx]["Close"]

            price = history.df.iloc[loc]["Close"]

            # TODO: Add a "allocation" parameter to the strategy to determine how much to buy/sell
            signals[rsi > self.upper_bound] = [TradeSignal(TransactionType.BUY, 1, price[security])
                                               for security in (rsi > self.upper_bound).keys()]
            signals[rsi < self.lower_bound] = [TradeSignal(TransactionType.SELL, 1, price[security])
                                               for security in (rsi < self.lower_bound).keys()]

        return signals
