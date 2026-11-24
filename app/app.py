from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"

st.set_page_config(page_title="Premier League Analytics", layout="wide")


@st.cache_data
def load(name):
    return pd.read_parquet(DATA_DIR / f"{name}.parquet")


form = load("mart_form")
home_away = load("mart_home_away")
attack_defense = load("mart_attack_defense")

st.title("Premier League Analytics")
st.caption("Pipeline: football-data.org API > Azure Blob > Snowflake > dbt > Streamlit")

tab1, tab2, tab3 = st.tabs(["Form vs table position", "Home vs away", "Attack vs defense"])

with tab1:
    common_game = int(form.groupby("team_id")["game_number"].max().min())
    snapshot = form[form["game_number"] == common_game]

    st.subheader("Recent form vs league position")
    st.caption(f"After {common_game} games per team. Points from the last 5 games, out of 15.")
    fig = px.scatter(
        snapshot,
        x="league_position",
        y="form_points_last5",
        text="team_name",
        labels={"league_position": "League position", "form_points_last5": "Points, last 5 games"},
    )
    fig.update_traces(textposition="top center", marker=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("League position over the season")
    top_teams = snapshot.nsmallest(6, "league_position")["team_name"].tolist()
    all_teams = sorted(form["team_name"].unique())
    picked = st.multiselect("Teams", all_teams, default=top_teams)
    plot_data = form[form["team_name"].isin(picked)].sort_values(["team_name", "game_number"])
    line = px.line(
        plot_data,
        x="game_number",
        y="league_position",
        color="team_name",
        markers=True,
        labels={"game_number": "Games played", "league_position": "League position"},
    )
    line.update_yaxes(autorange="reversed", range=[20.5, 0.5], dtick=1)
    st.plotly_chart(line, use_container_width=True)

with tab2:
    st.subheader("Points per game, home vs away")
    ha = home_away.copy()
    ha["venue"] = ha["is_home"].map({True: "Home", False: "Away"})
    order = ha.groupby("team_name")["points_per_game"].sum().sort_values(ascending=False).index
    fig = px.bar(
        ha,
        x="team_name",
        y="points_per_game",
        color="venue",
        barmode="group",
        category_orders={"team_name": list(order)},
        labels={"team_name": "", "points_per_game": "Points per game"},
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Attack vs defense")
    st.caption("Right of center scores more than the league average. Above center concedes fewer.")
    fig = px.scatter(
        attack_defense,
        x="attack_vs_league",
        y="defense_vs_league",
        text="team_name",
        labels={
            "attack_vs_league": "Goals scored per game vs league average",
            "defense_vs_league": "Goals conceded per game vs league average (higher is better)",
        },
    )
    fig.update_traces(textposition="top center", marker=dict(size=10))
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig, use_container_width=True)