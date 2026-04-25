# 📈 Stock Analyzer

A web app that analyzes stocks using fundamental and technical indicators — giving you a score, a recommendation (BUY / HOLD / SELL), and visual charts.

Built with **Flask** and deployed on **Render**.

---

## 🔗 Live Demo

> [https://flask-portfolio-j274.onrender.com](https://flask-portfolio-j274.onrender.com)  

---

## 🚀 Features

- Enter any valid stock ticker (e.g. `AAPL`, `GOOGL`, `TSLA`)
- View **fundamental metrics**: Revenue Growth, Profit Margin, Return on Equity, Debt-to-Equity
- View **technical indicators**: RSI, MACD
- Get an **overall score out of 10** and a **BUY / HOLD / SELL** recommendation
- Visual **RSI and MACD charts** generated per ticker
- 15-minute caching to reduce redundant API calls

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Data | yfinance |
| Charts | Matplotlib |
| Caching | Flask-Caching |
| Deployment | Render |

---

## 📁 Project Structure

```
stock-analyzer/
├── app.py                  # Flask routes and core analysis logic
├── requirements.txt        # Python dependencies
├── analysis/
│   ├── data.py             # Fetches stock data via yfinance
│   ├── fundamentals.py     # Revenue growth, margin, ROE, D/E ratio
│   ├── technicals.py       # RSI, MACD, Moving Averages
│   ├── scoring.py          # Scoring and recommendation logic
│   └── charts.py           # RSI and MACD chart generation
├── static/
│   └── style.css           # App styling
└── templates/
    ├── index.html          # Search page
    └── result.html         # Results page
```

---

## ⚙️ How Scoring Works

The overall score (0–10) is a weighted combination:

- **Fundamentals (60%)** — average of Revenue Growth, Profit Margin, ROE, and Debt-to-Equity scores
- **Technicals (40%)** — average of RSI and MACD scores

| Score | Recommendation |
|---|---|
| ≥ 7.5 | ✅ BUY |
| 5.5 – 7.4 | ➡️ HOLD |
| < 5.5 | ❌ SELL |

---

## 🖥️ Running Locally (VS Code)

**1. Clone the repository**
```bash
git clone https://github.com/vishakha408/flask-portfolio.git
cd stock-analyzer
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python app.py
```

**5. Open in browser**
```
http://127.0.0.1:5000
```

---

## ☁️ Deploying on Render

This app is configured to deploy on [Render](https://render.com) as a **Web Service**.

**Steps:**

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repository
4. Set the following:

| Setting | Value |
|---|---|
| Environment | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

5. Click **Deploy** — Render will build and host your app automatically.

> **Note:** Render's free tier spins down after inactivity. The first request after sleep may take ~30 seconds.

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**. It is not financial advice. Always do your own research before making investment decisions.
