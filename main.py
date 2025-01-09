import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import streamlit as st

competitions = sb.competitions()  # getting data of all available competitions

matches = sb.matches(competition_id=9, season_id=281)  # getting matches from Bundesliga season

l_matches = list(matches)  # list of all matches ofr selectbox

matches['game'] = matches['home_team'] + ' vs ' + matches['away_team']

games = list(matches['game'])  # list of all games for selectbox

selected_game = st.selectbox("Match:", games)

selected_game_id = matches.loc[matches['game'] == selected_game, 'match_id'].values[0]  # getting id of selected match
event = sb.events(match_id=selected_game_id)  # geting event from specific game

players = list(event.player.unique())  # list od players for selectbox
players = [p for p in players if p == p]  # removing nan values


# function for pass visualization
def pass_visualization(player):
    passes = event[(event.player == player) & (event.type == "Pass")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
    fig, ax = pitch.draw(figsize=(16, 11))
    ax_title = ax.set_title(f'{player} passes', fontsize=30)
    fig.set_facecolor('white')
    if len(passes) == 0:
        return fig
    else:
        passes[['x', 'y']] = passes['location'].apply(pd.Series)
        passes[['pass_end_x', 'pass_end_y']] = passes['pass_end_location'].apply(pd.Series)

        passes_good = passes[passes.pass_outcome.isna()]
        passes_assist = passes[passes.pass_goal_assist == True]

        # drawing passes
        pitch.arrows(passes.x, passes.y, passes.pass_end_x, passes.pass_end_y,
                     width=3, headwidth=8, headlength=5, color='red', ax=ax, zorder=2, label="Pass")
        # drawing good passes
        pitch.arrows(passes_good.x, passes_good.y, passes_good.pass_end_x, passes_good.pass_end_y,
                     width=3, headwidth=8, headlength=5, color='black', ax=ax, zorder=2, label="Pass")
        # drawing assist passes
        pitch.arrows(passes_assist.x, passes_assist.y, passes_assist.pass_end_x, passes_assist.pass_end_y,
                     width=5, headwidth=8, headlength=5, color='green', ax=ax, zorder=2, label="Pass")
        return fig


# function for shot visualization
def shot_visualization(player):
    shots = event[(event.player == player) & (event.type == "Shot")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
    fig, ax = pitch.draw(figsize=(16, 11))
    ax_title = ax.set_title(f'{player} shots', fontsize=30)
    fig.set_facecolor('white')
    if len(shots) == 0:
        return fig
    else:
        shots[['x', 'y']] = shots['location'].apply(pd.Series)
        shots_goal = shots[(shots.shot_outcome == "Goal")]
        shots_2d = shots[(shots.shot_outcome == "Blocked")]
        shots_on = shots[(shots.shot_outcome == "Saved")]
        shots_off = shots[(shots.shot_outcome == "Post") |
                         (shots.shot_outcome == "Off T")]
        if len(shots_on) > 0:
            shots_on[['shot_end_x', 'shot_end_y', 'shot_end_z']] = shots_on['shot_end_location'].apply(pd.Series)
            pitch.arrows(shots_on.x, shots_on.y, shots_on.shot_end_x, shots_on.shot_end_y,
                     width=3, headwidth=8, headlength=5, color='black', ax=ax, zorder=2, label="Pass")
        if len(shots_off) > 0:
            shots_off[['shot_end_x', 'shot_end_y', 'shot_end_z']] = shots_off['shot_end_location'].apply(pd.Series)
            pitch.arrows(shots_off.x, shots_off.y, shots_off.shot_end_x, shots_off.shot_end_y,
                     width=3, headwidth=8, headlength=5, color='red', ax=ax, zorder=2, label="Pass")
        if len(shots_goal) > 0:
            shots_goal[['shot_end_x', 'shot_end_y', 'shot_end_z']] = shots['shot_end_location'].apply(pd.Series)
            pitch.arrows(shots_goal.x, shots_goal.y, shots_goal.shot_end_x, shots_goal.shot_end_y,
                     width=5, headwidth=8, headlength=5, color='green', ax=ax, zorder=2, label="Pass")

        return fig


# function for won duels visualization
def duel_visualization(player):
    duels = event[(event.player == player) & (event.type == "Duel")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
    fig, ax = pitch.draw(figsize=(16, 11))
    ax_title = ax.set_title(f'{player} duels', fontsize=30)
    fig.set_facecolor('white')
    if len(duels) == 0:
        return fig
    else:
        duels[['x', 'y']] = duels['location'].apply(pd.Series)
        # drawing duel locations
        pitch.scatter(duels.x, duels.y, color='red', s=200, marker="o", ax=ax, zorder=2, label="Duel")
        duels_won = duels[(duels.duel_outcome == "Success In Play") | (duels.duel_outcome == "Won")
                         | (duels.duel_outcome == "Success") | (duels.duel_outcome == "Success Out")
                         | (duels.duel_outcome == "Success To Team") | (duels.duel_outcome == "Aerial Success")]
        duels_lost = duels[(duels.duel_outcome == "Lost In Play") | (duels.duel_outcome == "Lost")
                         | (duels.duel_outcome == "Lost Out") | (duels.duel_outcome == "Aerial Lost")]

        if len(duels_won) > 0:
            duels_won[['x', 'y']] = duels_won['location'].apply(pd.Series)
            pitch.scatter(duels_won.x, duels_won.y, color='green', s=200, marker="o", ax=ax, zorder=2, label="DuelWon")
        if len(duels_lost) > 0:
            duels_lost[['x', 'y']] = duels_lost['location'].apply(pd.Series)
            pitch.scatter(duels_lost.x, duels_lost.y, color='green', s=200, marker="o", ax=ax, zorder=2, label="DuelWon")
        return fig


# function for ball recovery visualization
def ball_recovery_visualization(player):
    player_br = event[
        (event.player == player) & (event.type == "Ball Recovery") & (event.ball_recovery_recovery_failure.isna())]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
    fig, ax = pitch.draw(figsize=(16, 11))
    ax_title = ax.set_title(f'{player} Succesful ball recoveries', fontsize=30)
    fig.set_facecolor('white')
    if len(player_br) == 0:
        return fig

    else:
        player_br[['x', 'y']] = player_br['location'].apply(pd.Series)
        # drawing ball recoveries location
        pitch.scatter(player_br.x, player_br.y, color='red', s=200, marker="o", ax=ax, zorder=2, label="Ball Recovery")
        return fig


chosen_player = st.selectbox("Players:", players)  # players selectbox
status = st.selectbox("Aspects :", ['Pass', 'Recovery'])

if status == 'Pass':
    st.pyplot(pass_visualization(chosen_player))
elif status == 'Shot':
    st.pyplot(shot_visualization(chosen_player))
else:
    if status == 'Recovery':
        st.pyplot(ball_recovery_visualization(chosen_player))
    else:
        st.pyplot(duel_visualization(chosen_player))

# print(event)
