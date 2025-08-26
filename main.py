
import yfinance as yf
import pandas as pd
import numpy as np

# Step 1: Download data
data = yf.download("GC=F", interval="1h", period="60d")

# Step 2: Calculate RSI
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data['Close'])

# Step 3: Define signals (example: RSI < 30 = Buy, RSI > 70 = Sell)
data['buy_signal'] = (data['RSI'] < 30)
data['sell_signal'] = (data['RSI'] > 70)

print("Buy signals found:", data['buy_signal'].sum())
print("Sell signals found:", data['sell_signal'].sum())

# Step 4: Simulate trades
in_trade = False
entry_price = 0
entry_date = None
trades = []

for i in range(len(data)):
    price = data['Close'].iloc[i]
    date = data.index[i]

    if data['buy_signal'].iloc[i] and not in_trade:
        in_trade = True
        entry_price = price
        entry_date = date

    elif data['sell_signal'].iloc[i] and in_trade:
        in_trade = False
        exit_price = price
        exit_date = date
        profit_pct = ((exit_price - entry_price) / entry_price) * 100

        trades.append({
            'Entry Date': entry_date,
            'Exit Date': exit_date,
            'Entry Price': entry_price,
            'Exit Price': exit_price,
            'Profit %': float(round(profit_pct, 2))   # ✅ force numeric
        })

# Step 5: Analyze results
trades_df = pd.DataFrame(trades)

if not trades_df.empty:
    trades_df['Profit %'] = pd.to_numeric(trades_df['Profit %'], errors='coerce')

    total_trades = len(trades_df)
    winning_trades = trades_df[trades_df['Profit %'] > 0]
    losing_trades = trades_df[trades_df['Profit %'] <= 0]
    win_rate = len(winning_trades) / total_trades * 100
    avg_profit = trades_df['Profit %'].mean()

    print("\nTrade History:")
    print(trades_df)

    print("\nSummary:")
    print(f"Total Trades: {total_trades}")
    print(f"Winning Trades: {len(winning_trades)}")
    print(f"Losing Trades: {len(losing_trades)}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Average Profit per Trade: {avg_profit:.2f}%")
else:
    print("No trades executed in this period.")

import matplotlib.pyplot as plt

# Plot Close Price and RSI
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Plot price
ax1.plot(data.index, data['Close'], label='Gold Price', color='blue')
ax1.set_title('Gold Price with Buy/Sell Signals')
ax1.set_ylabel('Price (USD)')
ax1.grid(True)

# Highlight buy signals
ax1.scatter(data.index[data['buy_signal']], 
            data['Close'][data['buy_signal']], 
            marker='^', color='green', label='Buy Signal', s=100)

# Highlight sell signals
ax1.scatter(data.index[data['sell_signal']], 
            data['Close'][data['sell_signal']], 
            marker='v', color='red', label='Sell Signal', s=100)

ax1.legend()

# Plot RSI
ax2.plot(data.index, data['RSI'], label='RSI', color='orange')
ax2.axhline(70, color='red', linestyle='--', label='Overbought (70)')
ax2.axhline(30, color='green', linestyle='--', label='Oversold (30)')
ax2.set_title('Relative Strength Index (RSI)')
ax2.set_ylabel('RSI Value')
ax2.set_xlabel('Date')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()

if not trades_df.empty:
    plt.figure(figsize=(12,6))
    plt.bar(trades_df['Entry Date'], trades_df['Profit %'], color=trades_df['Profit %'].apply(lambda x: 'green' if x>0 else 'red'))
    plt.title('Profit % per Trade')
    plt.xlabel('Entry Date')
    plt.ylabel('Profit %')
    plt.grid(True)
    plt.show()




