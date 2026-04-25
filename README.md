<div align="center">

# 📈 Stock Analyzer

**AI-powered stock analysis with fundamentals, technicals, charts, and Gemini insights.**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Render-46E3B7?style=for-the-badge)](https://flask-portfolio-j274.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Gemini_AI-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)

</div>

---

## ✨ What It Does

Enter any stock ticker and get a full analysis in seconds:

| Feature | Description |
|---|---|
| 📊 **Score** | Overall score out of 10 based on fundamentals + technicals |
| 🎯 **Recommendation** | Clear BUY / HOLD / SELL signal |
| 📈 **Fundamentals** | Revenue Growth, Profit Margin, ROE, Debt-to-Equity |
| 📉 **Technicals** | RSI and MACD with visual charts |
| 🤖 **AI Insights** | Gemini interprets the data — not just restates it |
| ⚡ **Caching** | 15-minute cache to avoid redundant API calls |

---

## 🤖 AI Analysis — What Makes It Different

Most tools just show you numbers. This app uses **Google Gemini** to interpret them:

> *"Is the high debt justified by strong ROE? Are RSI and MACD confirming each other or diverging? What's the biggest risk right now?"*

The AI summary answers in **4-5 bullet points**:
- 💡 What the fundamentals tell together as a story
- 📡 Whether technical momentum confirms or contradicts fundamentals
- ⚠️ Biggest risk + biggest opportunity
- 👤 What type of investor this stock suits

---

## ⚙️ How Scoring Works

```
Overall Score (0–10)
├── Fundamentals (60%)
│   ├── Revenue Growth
│   ├── Profit Margin
│   ├── Return on Equity
│   └── Debt-to-Equity
└── Technicals (40%)
    ├── RSI
    └── MACD
```

| Score | Signal |
|:---:|:---:|
| ≥ 7.5 | ✅ BUY |
| 5.5 – 7.4 | ➡️ HOLD |
| < 5.5 | ❌ SELL |

---

## 🛠️ Tech Stack

```
Frontend    →  HTML, CSS (Jinja2 templates)
Backend     →  Python, Flask
Data        →  yfinance
Charts      →  Matplotlib
AI          →  Google Gemini API (gemini-2.5-flash)
Caching     →  Flask-Caching
Deployment  →  Render + Gunicorn
```

---

## 📁 Project Structure

```
stock-analyzer/
│
├── app.py                  # Core Flask routes & analysis logic
├── ai_summary.py           # Gemini AI summary generation
├── requirements.txt        # Dependencies
│
├── analysis/
│   ├── data.py             # yfinance data fetching
│   ├── fundamentals.py     # Revenue, margin, ROE, D/E
│   ├── technicals.py       # RSI, MACD
│   ├── scoring.py          # Score + recommendation logic
│   └── charts.py           # Chart generation
│
├── static/
│   └── style.css           # Styling
│
└── templates/
    ├── index.html          # Search page
    └── result.html         # Results page
```

---

## 🖥️ Run Locally

**1. Clone & navigate**
```bash
git clone https://github.com/vishakha408/flask-portfolio.git
cd stock-analyzer
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Gemini API key**

Create a `.env` file in the root:
```
GEMINI_API_KEY=your-key-here
```
Get a free key → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**5. Run**
```bash
python app.py
```
Open → `http://127.0.0.1:5000`

---

## ☁️ Deploy on Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo and set:

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

4. Under **Environment Variables** add:

| Key | Value |
|---|---|
| `GEMINI_API_KEY` | your-gemini-key |

5. Hit **Deploy** 🚀

> 💤 Free tier sleeps after inactivity — first request may take ~30 seconds to wake up.

---

<div align="center">

⚠️ **Disclaimer:** For educational purposes only. Not financial advice. Always do your own research.

</div>
