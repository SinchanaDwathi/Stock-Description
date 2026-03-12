from flask import Flask, render_template, request
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io, base64
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

POPULAR_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "WIPRO.NS"
]

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        if hist.empty:
            return None, None
        info = stock.info
        return hist, info
    except Exception:
        return None, None

def predict_next_day(hist):
    closes = hist['Close'].values
    X = np.arange(len(closes)).reshape(-1, 1)
    y = closes
    model = LinearRegression()
    model.fit(X, y)
    next_x = np.array([[len(closes)]])
    predicted = model.predict(next_x)[0]
    return round(float(predicted), 2)

def get_trend(hist):
    last_30 = hist['Close'].tail(30)
    if len(last_30) < 2:
        return "neutral"
    start_price = last_30.iloc[0]
    end_price = last_30.iloc[-1]
    return "up" if end_price > start_price else "down"

def generate_graph(hist, predicted_price, ticker):
    fig, ax = plt.subplots(figsize=(11, 4.5))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    dates = hist.index
    closes = hist['Close'].values

    # Gradient-like fill
    ax.fill_between(dates, closes, alpha=0.15, color='#00d4ff')
    ax.plot(dates, closes, color='#00d4ff', linewidth=1.8, label='Closing Price', zorder=3)

    # Predicted point
    next_date = dates[-1] + timedelta(days=1)
    ax.scatter([next_date], [predicted_price], color='#ff6b35', s=100, zorder=5, label=f'Predicted: ₹{predicted_price:.2f}')
    ax.annotate(f'  ${predicted_price:.2f}', xy=(next_date, predicted_price),
                color='#ff6b35', fontsize=10, fontweight='bold', va='center')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30, color='#8b9ab0', fontsize=9)
    plt.yticks(color='#8b9ab0', fontsize=9)

    for spine in ax.spines.values():
        spine.set_edgecolor('#1e2a3a')

    ax.grid(color='#1e2a3a', linestyle='--', linewidth=0.6, alpha=0.8)
    ax.set_title(f'{ticker.upper()} — 1 Year Price History', color='#e8f4fd', fontsize=13, fontweight='bold', pad=14)
    ax.set_ylabel('Price (USD/INR)', color='#8b9ab0', fontsize=10)
    ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='#c9d1d9', fontsize=9)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=130, bbox_inches='tight', facecolor='#0d1117')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_b64

def get_downtrend_stocks():
    downtrend = []
    for ticker in POPULAR_STOCKS:
        hist, info = get_stock_data(ticker)
        if hist is not None and len(hist) >= 30:
            trend = get_trend(hist)
            if trend == "down":
                last_price = round(float(hist['Close'].iloc[-1]), 2)
                change = round(float(hist['Close'].iloc[-1] - hist['Close'].iloc[-30]), 2)
                pct = round((change / hist['Close'].iloc[-30]) * 100, 2)
                name = info.get('shortName', ticker) if info else ticker
                downtrend.append({
                    "ticker": ticker,
                    "name": name,
                    "price": last_price,
                    "change": change,
                    "pct": pct
                })
    return downtrend

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    downtrend_stocks = get_downtrend_stocks()

    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip().upper()
        if not ticker:
            error = "Please enter a stock ticker symbol."
        else:
            hist, info = get_stock_data(ticker)
            if hist is None or len(hist) < 30:
                error = f"Could not fetch data for '{ticker}'. Check the symbol and try again."
            else:
                current_price = round(float(hist['Close'].iloc[-1]), 2)
                predicted_price = predict_next_day(hist)
                trend = get_trend(hist)
                graph_b64 = generate_graph(hist, predicted_price, ticker)

                name = info.get('shortName', ticker) if info else ticker
                currency = info.get('currency', 'USD') if info else 'USD'

                if trend == "up":
                    suggestion = "📈 Uptrend – May be good to invest"
                    suggestion_class = "uptrend"
                else:
                    suggestion = "📉 Downtrend – Be cautious / avoid investing"
                    suggestion_class = "downtrend"

                price_diff = round(predicted_price - current_price, 2)
                price_diff_pct = round((price_diff / current_price) * 100, 2)

                result = {
                    "ticker": ticker,
                    "name": name,
                    "currency": currency,
                    "current_price": current_price,
                    "predicted_price": predicted_price,
                    "price_diff": price_diff,
                    "price_diff_pct": price_diff_pct,
                    "suggestion": suggestion,
                    "suggestion_class": suggestion_class,
                    "graph": graph_b64
                }

    return render_template('index.html', result=result, error=error, downtrend_stocks=downtrend_stocks)

if __name__ == '__main__':
    app.run(debug=True)
