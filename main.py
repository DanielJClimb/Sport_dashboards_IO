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
        #pitch.text(5,5,len(passes),ax)
        #pitch.text(5,10,len(passes_good),ax)
        #pitch.text(5,15,len(passes_assist),ax)

        # drawing passes
        pitch.arrows(passes.x, passes.y, passes.pass_end_x, passes.pass_end_y,
                     width=3, headwidth=8, headlength=5, color='red', ax=ax, zorder=2, label="Pass")
        # drawing good passes
        pitch.arrows(passes_good.x, passes_good.y, passes_good.pass_end_x, passes_good.pass_end_y,
                     width=3, headwidth=8, headlength=5, color='green', ax=ax, zorder=2, label="Pass")
        # drawing assist passes
        pitch.arrows(passes_assist.x, passes_assist.y, passes_assist.pass_end_x, passes_assist.pass_end_y,
                     width=5, headwidth=8, headlength=5, color='black', ax=ax, zorder=2, label="Pass")
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

else:
    st.pyplot(ball_recovery_visualization(chosen_player))

# print(event)
