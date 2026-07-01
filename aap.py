import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IPL Dashboard", layout="wide", page_icon="🏏")

# Load data
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

st.title("🏏 IPL Stats Dashboard")
st.markdown("Complete IPL analysis — team performance, player stats, and more.")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")
seasons = sorted(matches['season'].unique())
selected_season = st.sidebar.selectbox("Select Season", ["All Seasons"] + list(seasons))

if selected_season != "All Seasons":
    filtered_matches = matches[matches['season'] == selected_season]
else:
    filtered_matches = matches

match_ids = filtered_matches['id'].tolist()
filtered_deliveries = deliveries[deliveries['match_id'].isin(match_ids)]

# ---------------- TOP METRIC CARDS ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", len(filtered_matches))
col2.metric("Total Teams", filtered_matches['winner'].nunique())
col3.metric("Total Seasons", matches['season'].nunique())
col4.metric("Total Sixes", int(filtered_deliveries[filtered_deliveries['batsman_runs']==6].shape[0]))

st.divider()

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Teams", "🏏 Batting", "🎯 Bowling", "🤝 Head-to-Head", "🔍 Player Search"])

# ---- TAB 1: TEAMS ----
with tab1:
    st.header("Team Wins")
    team_wins = filtered_matches['winner'].value_counts().reset_index()
    team_wins.columns = ['Team', 'Wins']
    fig1 = px.bar(team_wins, x='Team', y='Wins', color='Wins', color_continuous_scale='Blues')
    st.plotly_chart(fig1, use_container_width=True)

    st.header("Toss Impact: Does Winning Toss Help?")
    toss_match_same = filtered_matches[filtered_matches['toss_winner'] == filtered_matches['winner']]
    toss_win_pct = round(len(toss_match_same) / len(filtered_matches) * 100, 2) if len(filtered_matches) > 0 else 0
    st.write(f"Teams that won the toss also won the match **{toss_win_pct}%** of the time.")

    st.header("Man of the Match — Top 10")
    motm = filtered_matches['player_of_match'].value_counts().head(10).reset_index()
    motm.columns = ['Player', 'Awards']
    fig_motm = px.bar(motm, x='Player', y='Awards', color='Awards', color_continuous_scale='Purples')
    st.plotly_chart(fig_motm, use_container_width=True)

# ---- TAB 2: BATTING ----
with tab2:
    st.header("Top 10 Run Scorers")
    top_runs = filtered_deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
    top_runs.columns = ['Player', 'Runs']
    fig2 = px.bar(top_runs, x='Player', y='Runs', color='Runs', color_continuous_scale='Oranges')
    st.plotly_chart(fig2, use_container_width=True)

    st.header("Top 10 Strike Rates (min 200 balls faced)")
    balls_faced = filtered_deliveries.groupby('batter')['ball'].count()
    runs_scored = filtered_deliveries.groupby('batter')['batsman_runs'].sum()
    sr_df = pd.DataFrame({'Balls': balls_faced, 'Runs': runs_scored})
    sr_df = sr_df[sr_df['Balls'] >= 200]
    sr_df['Strike Rate'] = round((sr_df['Runs'] / sr_df['Balls']) * 100, 2)
    top_sr = sr_df.sort_values('Strike Rate', ascending=False).head(10).reset_index()
    fig_sr = px.bar(top_sr, x='batter', y='Strike Rate', color='Strike Rate', color_continuous_scale='Reds')
    st.plotly_chart(fig_sr, use_container_width=True)

# ---- TAB 3: BOWLING ----
with tab3:
    st.header("Top 10 Wicket Takers")
    wickets = filtered_deliveries.dropna(subset=['player_dismissed'])
    top_wickets = wickets['bowler'].value_counts().head(10).reset_index()
    top_wickets.columns = ['Bowler', 'Wickets']
    fig3 = px.bar(top_wickets, x='Bowler', y='Wickets', color='Wickets', color_continuous_scale='Greens')
    st.plotly_chart(fig3, use_container_width=True)

    st.header("Top 10 Best Economy Rates (min 120 balls bowled)")
    balls_bowled = filtered_deliveries.groupby('bowler')['ball'].count()
    runs_conceded = filtered_deliveries.groupby('bowler')['total_runs'].sum()
    eco_df = pd.DataFrame({'Balls': balls_bowled, 'Runs': runs_conceded})
    eco_df = eco_df[eco_df['Balls'] >= 120]
    eco_df['Economy'] = round((eco_df['Runs'] / eco_df['Balls']) * 6, 2)
    best_eco = eco_df.sort_values('Economy', ascending=True).head(10).reset_index()
    fig_eco = px.bar(best_eco, x='bowler', y='Economy', color='Economy', color_continuous_scale='Teal')
    st.plotly_chart(fig_eco, use_container_width=True)

# ---- TAB 4: HEAD TO HEAD ----
with tab4:
    st.header("Head-to-Head Comparison")
    all_teams = sorted(matches['team1'].unique())
    c1, c2 = st.columns(2)
    team_a = c1.selectbox("Team A", all_teams, index=0)
    team_b = c2.selectbox("Team B", all_teams, index=1)

    h2h = matches[((matches['team1']==team_a) & (matches['team2']==team_b)) | ((matches['team1']==team_b) & (matches['team2']==team_a))]
    st.write(f"Total matches played between **{team_a}** and **{team_b}**: {len(h2h)}")

    h2h_wins = h2h['winner'].value_counts().reset_index()
    h2h_wins.columns = ['Team', 'Wins']
    if not h2h_wins.empty:
        fig_h2h = px.pie(h2h_wins, names='Team', values='Wins', title="Head-to-Head Win Share")
        st.plotly_chart(fig_h2h, use_container_width=True)
    else:
        st.write("No matches found between these teams.")

# ---- TAB 5: PLAYER SEARCH ----
with tab5:
    st.header("Search Any Player")
    all_players = sorted(deliveries['batter'].unique())
    selected_player = st.selectbox("Choose a Player", all_players)

    player_balls = deliveries[deliveries['batter'] == selected_player]
    total_runs = player_balls['batsman_runs'].sum()
    total_balls = player_balls.shape[0]
    fours = player_balls[player_balls['batsman_runs']==4].shape[0]
    sixes = player_balls[player_balls['batsman_runs']==6].shape[0]
    strike_rate = round((total_runs/total_balls)*100, 2) if total_balls > 0 else 0

    p1, p2, p3, p4, p5 = st.columns(5)
    p1.metric("Total Runs", total_runs)
    p2.metric("Balls Faced", total_balls)
    p3.metric("Fours", fours)
    p4.metric("Sixes", sixes)
    p5.metric("Strike Rate", strike_rate)

    # Wickets if player also bowled
    player_wickets = deliveries[(deliveries['bowler']==selected_player) & (deliveries['player_dismissed'].notna())].shape[0]
    if player_wickets > 0:
        st.write(f"**{selected_player}** has also taken **{player_wickets} wickets** as a bowler.")

