# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import yfinance as yf

app = FastAPI()

# Allow CORS (important for frontend apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock/{symbol}")
def get_stock_data(symbol: str):
    stock = yf.Ticker(symbol.upper())

    try:
        current_price = stock.info.get("regularMarketPrice")
        open_price = stock.info.get("regularMarketOpen")
    except Exception as e:
        return {"error": f"Error fetching stock info: {str(e)}"}

    try:
        history = stock.history(period="5y")
        price_1m = history.iloc[-21]["Close"] if len(history) >= 21 else None
        price_1y = history.iloc[-252]["Close"] if len(history) >= 252 else None
        price_3y = history.iloc[-756]["Close"] if len(history) >= 756 else None
        price_5y = history.iloc[0]["Close"] if len(history) >= 1000 else None
    except Exception as e:
        return {"error": f"Error fetching history: {str(e)}"}

    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "open_price": open_price,
        "price_1m": price_1m,
        "price_1y": price_1y,
        "price_3y": price_3y,
        "price_5y": price_5y,
    }

# This is the AWS Lambda handler
handler = Mangum(app)
