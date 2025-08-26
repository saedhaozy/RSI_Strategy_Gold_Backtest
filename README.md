# RSI_Strategy_Gold_Backtest
This is my first trading strategy as I begin my journey in algorithmic trading. The goal is to test a simple, rules-based system using the Relative Strength Index (RSI) indicator on Gold futures (GC=F). The strategy is meant to help me understand how to build, test, and evaluate trading strategies step by step 
Indicator Used: Relative Strength Index (RSI) with a period of 14.
Buy Rule: Enter a trade when RSI falls below 30 (oversold condition).
Sell Rule: Exit the trade when RSI rises above 70 (overbought condition).
Trade Direction: Long-only strategy (buy → sell).
Data Used: Gold Futures (GC=F) with a 1-hour timeframe over the past 60 days.
Why RSI?
The RSI is a momentum oscillator that measures the speed and change of price
movements.
Values below 30 suggest that the market may be oversold, and a reversal to the upside
could occur.
Values above 70 suggest that the market may be overbought, and a reversal to the
downside could occur.
This makes RSI a simple but effective tool to identify possible entry and exit points.
