# StockSense – ML Stock Price Prediction Dashboard
### MCA Student Project | Flask + yfinance + scikit-learn

---

## 📁 Project Structure

```
StockPrediction/
├── app.py
├── requirements.txt
├── README.md
└── templates/
    └── index.html
```

---

## ⚙️ Installation & Running Locally

```bash
# 1. Install dependencies
pip install flask yfinance scikit-learn numpy matplotlib gunicorn

# 2. Run the app
python app.py

# 3. Open in browser
http://127.0.0.1:5000
```

---

## 🚀 Deployment

### Render (render.com)
1. Push project to GitHub
2. Create a new "Web Service" on Render
3. Set Start Command: `gunicorn app:app`
4. Add requirements.txt – Render installs automatically

### Replit
1. Upload files to a new Repl (Python template)
2. Install packages via Shell: `pip install -r requirements.txt`
3. Click Run – Replit auto-detects Flask

### PythonAnywhere
1. Upload files via "Files" tab
2. Create a new Web App (Flask)
3. Point WSGI config to `app.py`
4. Install packages in a Bash console

---

## 🔬 How It Works

| Component | Technology |
|-----------|-----------|
| Backend | Flask (Python) |
| Stock Data | yfinance (Yahoo Finance API) |
| ML Model | Linear Regression (scikit-learn) |
| Graph | matplotlib → base64 embedded |
| Frontend | HTML5 + CSS3 (responsive) |

### Prediction Logic
- Fetches 1 year of closing price history
- Uses day index (0, 1, 2 … N) as the feature `X`
- Fits `LinearRegression` and predicts for day `N+1`

### Trend / Suggestion Logic
- Compares closing price 30 trading days ago vs today
- Positive change → "Uptrend – May be good to invest"
- Negative change → "Downtrend – Be cautious / avoid investing"

---

## ⚠️ Disclaimer
This project is for academic/educational purposes only.
It is NOT financial advice. Do not make real investment decisions based on this tool.
"# Stock-Description" 
