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
    passes = event[(event.player == player) & (event.type == "Pass") & (event.pass_outcome.isna())]
    # print(passes.pass_outcome)
    # print(passes.pass_type)
    # print(passes)
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

        # drawing passes
        pitch.arrows(passes.x, passes.y, passes.pass_end_x, passes.pass_end_y,
                     width=3, headwidth=8, headlength=5, color='red', ax=ax, zorder=2, label="Pass")
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


# function for dispossessed visualization
def dispossessed_visualization(player):
    player_d = event[
        (event.player == player) & (event.type == "Dispossessed")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
    fig, ax = pitch.draw(figsize=(16, 11))
    ax_title = ax.set_title(f'{player} Dispossessed', fontsize=30)
    fig.set_facecolor('white')
    if len(player_d) == 0:
        return fig

    else:
        player_d[['x', 'y']] = player_d['location'].apply(pd.Series)
        # drawing ball dispossessed location
        pitch.scatter(player_d.x, player_d.y, color='red', s=200, marker="o", ax=ax, zorder=2, label="Dispossessed")
        return fig


# function for won duels visualization
def duel_visualization(player):
    duels = event[(event.player == player) & (event.type == "Duel")]
    # creating pitch
    print(duels.duel_outcome)
    print(duels.duel_type)
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
    fig, ax = pitch.draw(figsize=(16, 11))
    ax_title = ax.set_title(f'{player} duels', fontsize=30)
    fig.set_facecolor('white')
    if len(duels) == 0:
        return fig
    else:
        # pitch.text(5, 5, len(duels), ax)
        # pitch.text(5, 10, duels.duel_outcome, ax)
        duels[['x', 'y']] = duels['location'].apply(pd.Series)
        # drawing duel locations
        pitch.scatter(duels.x, duels.y, color='red', s=200, marker="o", ax=ax, zorder=2, label="Duel")
        duels_won = duels[(duels.duel_type == "Tackle")
                      & ((duels.duel_outcome == "Success In Play") | (duels.duel_outcome == "Won")
                         | (duels.duel_outcome == "Success") | (duels.duel_outcome == "Success Out")
                         | (duels.duel_outcome == "Success To Team"))]
        # pitch.text(10, 5, len(duels_won), ax)
        if len(duels_won) > 0:
            duels_won[['x', 'y']] = duels_won['location'].apply(pd.Series)
            pitch.scatter(duels_won.x, duels_won.y, color='green', s=200, marker="o", ax=ax, zorder=2, label="DuelWon")
        return fig

# function for shot visualization
def shot_visualization(player):
    player_shots = event[(event.player == player) & (event.type == "Shot")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
    fig, ax = pitch.draw(figsize=(16, 11))
    ax_title = ax.set_title(f'{player} shots', fontsize=30)
    fig.set_facecolor('white')
    if len(player_shots) == 0:
        pitch.scatter(0, 0, color='red', s=200, marker="o", ax=ax, zorder=2, label="Shot")
        return fig
    else:
        pitch.scatter(0, 0, color='blue', s=200, marker="o", ax=ax, zorder=2, label="Shot")
        player_shots[['x', 'y']] = player_shots['location'].apply(pd.Series)
        pitch.scatter(player_shots.x, player_shots.y, color='red', s=200, marker="o", ax=ax, zorder=2, label="Shot")
        # player_shots[['pass_end_x', 'pass_end_y']] = player_shots['pass_end_location'].apply(pd.Series)

        # drawing shots
        # pitch.arrows(player_shots.x, player_shots.y, player_shots.pass_end_x, player_shots.pass_end_y,
        #              width=3, headwidth=8, headlength=5, color='green', ax=ax, zorder=2, label="Pass")
        return fig


chosen_player = st.selectbox("Players:", players)  # players selectbox
status = st.selectbox("Aspects :", ['Pass', 'Recovery', 'Duel', 'Dispossessed', 'Shot'])

if status == 'Pass':
    st.pyplot(pass_visualization(chosen_player))

elif status == 'Dispossessed':
    st.pyplot(dispossessed_visualization(chosen_player))
elif status == 'Shot':
    st.pyplot(shot_visualization(chosen_player))
else:
    if status == 'Recovery':
        st.pyplot(ball_recovery_visualization(chosen_player))
    else:
        st.pyplot(duel_visualization(chosen_player))

# print(event)