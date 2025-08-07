from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/stock/<symbol>", methods=["GET"])
def get_stock_data(symbol):
    stock = yf.Ticker(symbol.upper())

    # Current price
    try:
        current_price = stock.info.get("regularMarketPrice", None)
        open_price = stock.info.get("regularMarketOpen", None)
    except Exception as e:
        return jsonify({"error": f"Error fetching stock info: {str(e)}"}), 500

    # Historical prices
    try:
        history = stock.history(period="5y")
        price_1m = history.iloc[-21]["Close"] if len(history) >= 21 else None
        price_1y = history.iloc[-252]["Close"] if len(history) >= 252 else None
        price_3y = history.iloc[-756]["Close"] if len(history) >= 756 else None
        price_5y = history.iloc[0]["Close"] if len(history) >= 1000 else None
    except Exception as e:
        return jsonify({"error": f"Error fetching history: {str(e)}"}), 500

    return jsonify({
        "symbol": symbol.upper(),
        "current_price": current_price,
        "open_price": open_price,
        "price_1m": price_1m,
        "price_1y": price_1y,
        "price_3y": price_3y,
        "price_5y": price_5y,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
