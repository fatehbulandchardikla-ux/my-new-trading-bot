import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from telegram import Bot
import asyncio

# Settings
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TOKEN)

def get_data(symbol):
    df = yf.download(symbol, period="1d", interval="1m")
    return df

def analyze(df):
    df['EMA_9'] = ta.ema(df['Close'], length=9)
    df['EMA_21'] = ta.ema(df['Close'], length=21)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    return df.iloc[-1] # Sirf last candle

async def run_bot():
    symbol = "GC=F" # Gold
    while True:
        try:
            data = get_data(symbol)
            row = analyze(data)
            
            # Logic
            if row['EMA_9'] > row['EMA_21'] and row['RSI'] > 50:
                await bot.send_message(chat_id=CHAT_ID, text=f"🚀 Buy Signal Gold: {row['Close']}")
            elif row['EMA_9'] < row['EMA_21'] and row['RSI'] < 50:
                await bot.send_message(chat_id=CHAT_ID, text=f"📉 Sell Signal Gold: {row['Close']}")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await asyncio.sleep(60) # 1 minute wait

if __name__ == "__main__":
    asyncio.run(run_bot())
  
