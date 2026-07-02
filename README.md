# 🏏 IPL Cricket Stats Dashboard

An interactive web dashboard built with Python and Streamlit to explore IPL (Indian Premier League) statistics — team performance, top run scorers, top wicket takers, toss impact, head-to-head records, and individual player search.

---

## 📌 Overview

This project analyzes ball-by-ball and match-level IPL data (2008–2024) and presents it through an easy-to-use, filterable web dashboard. It was built as an end-to-end data analytics project — from raw CSV data to a deployed interactive application.

---

## ✨ Features

- Season filter — view stats for a specific IPL season or all seasons combined
- Summary metrics — total matches, total teams, total seasons, total sixes
- Team Wins — bar chart of match wins per team
- Toss Impact — win percentage when a team wins the toss
- Man of the Match — top award winners
- Top Run Scorers and Top Strike Rates
- Top Wicket Takers and Best Economy Rates
- Head-to-Head Comparison — pick any two teams and see their win record
- Player Search — full career stats (runs, balls faced, fours, sixes, strike rate, wickets) for any player

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| Data Handling | Pandas |
| Visualization | Plotly Express |
| Web Framework | Streamlit |
| Dataset | Kaggle – IPL Complete Dataset |

---

## 📂 Project Structure

ipl_dashboard/
├── aap.py          (Main Streamlit dashboard application)
├── matches.csv     (Match-level dataset)
├── deliveries.csv  (Ball-by-ball dataset)
└── README.md       (Project documentation)

---

## 🚀 How to Run Locally

1. Clone this repository
   git clone https://github.com/Varsha2719/ipl-dashboard.git
   cd ipl-dashboard

2. Install the required libraries
   pip install pandas streamlit plotly

3. Run the app
   streamlit run aap.py

4. Open the link shown in the terminal (usually http://localhost:8501) in your browser.

---

## 📊 Sample Insights

- Mumbai Indians have the most match wins in IPL history.
- Virat Kohli leads the all-time run-scoring charts.
- Teams winning the toss have historically gone on to win a significant share of matches.

---

## 🔮 Future Scope

- Live match data integration via a cricket API
- Venue-wise and city-wise performance analysis
- Player comparison tool
- Public deployment on Streamlit Community Cloud

---

## 👩‍💻 Author

Varsha Gangwar