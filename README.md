# 📈 StockSense – ML Stock Price Prediction Dashboard

> A Flask web application that fetches real-time stock data, predicts the next day's closing price using Linear Regression, and visualises 1-year price history 

##  Features

-  **Search any stock** — supports US tickers (`AAPL`, `MSFT`, `GOOGL`) and Indian NSE tickers (`TCS.NS`, `INFY.NS`, `RELIANCE.NS`)
-  **Live price** — fetched in real time via Yahoo Finance (`yfinance`)
-  **ML Prediction** — Linear Regression model predicts the next day's closing price
-  **1-Year Price Chart** — dark-themed matplotlib graph embedded directly in the page
-  **Predicted point highlighted** on the chart
-  **Investment suggestion** based on the last 30-day trend (Uptrend / Downtrend)
-  **Stocks to Avoid sidebar** — auto-scans 10 popular stocks and flags those in a downtrend
-  **Fully responsive** — works on mobile, tablet, and desktop

---

## 🗂️ Project Structure

```
StockPrediction/
├── app.py                  # Flask backend – routes, ML model, chart generation
├── requirements.txt        # Python dependencies
├── README.md
└── templates/
    └── index.html          # Responsive dashboard UI (HTML + CSS + JS)
```

---

## ⚙️ Installation & Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/StockPrediction.git
cd StockPrediction
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask yfinance scikit-learn numpy matplotlib gunicorn
```

### 4. Run the app

```bash
python app.py
```

### 5. Open in your browser

```
http://127.0.0.1:5000
```

---

## 🔬 How It Works

### Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask (Python) |
| Stock Data | yfinance (Yahoo Finance API) |
| Machine Learning | Linear Regression — scikit-learn |
| Data Processing | NumPy |
| Chart Generation | matplotlib → base64 PNG |
| Frontend | HTML5 + CSS3 (CSS Grid, responsive) |

### ML Prediction Logic

1. Fetches **1 year** of daily closing price history for the entered ticker
2. Creates a sequential feature `X = [0, 1, 2, … N]` (day index)
3. Fits a **`LinearRegression`** model on `(X, closing_prices)`
4. Predicts for day `N+1` → displayed as the **next-day price forecast**

### Trend & Investment Suggestion

- Compares the closing price **30 trading days ago** vs **today**
- Positive change → `📈 Uptrend – May be good to invest`
- Negative change → `📉 Downtrend – Be cautious / avoid investing`

---

## 📦 Dependencies

```
flask
yfinance
scikit-learn
numpy
matplotlib
gunicorn
```

---


## ⚠️ Disclaimer

This project is built **for academic and educational purposes only**.  
It is **not financial advice**. Do not make real investment decisions based on predictions from this tool.  
Stock markets are subject to risk — always consult a qualified financial advisor.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
