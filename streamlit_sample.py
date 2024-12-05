# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:34:40 2024

@author: danio
"""

import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import streamlit as st

competitions = sb.competitions() # getting data of all avaible competitions

matches = sb.matches(competition_id = 9, season_id = 281) # getting matches from Bundesliga season

matches['game'] = matches['home_team'] + ' vs ' + matches['away_team']

# getting list of games id
matches_id = list(matches['match_id'])

event = sb.events(match_id = 3895302) # geting event from specific game

players = list(event.player.unique())
players = [p for p in players if p ==p]

# function for pass visualization
def pass_visualization(player):
    player_passes = event[(event.player == player) & (event.type == "Pass") & (event.pass_outcome.isna())]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2,line_color='black')
    fig, ax = pitch.draw(figsize=(16,11))
    ax_title = ax.set_title(f'{player} passes', fontsize = 30)
    fig.set_facecolor('white')
    if  len(player_passes) == 0:
        return fig
    else:
        player_passes[['x', 'y']] = player_passes['location'].apply(pd.Series)
        player_passes[['pass_end_x', 'pass_end_y']] = player_passes['pass_end_location'].apply(pd.Series)

        # drawing passes
        pitch.arrows(player_passes.x, player_passes.y, player_passes.pass_end_x, player_passes.pass_end_y,
                    width=3, headwidth=8, headlength=5, color = 'green', ax = ax, zorder = 2, label = "Pass")
        return fig

def ball_recovery_visualization(player):
    player_br = event[(event.player == player) & (event.type == "Ball Recovery") & (event.ball_recovery_recovery_failure.isna())]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2,line_color='black')
    fig, ax = pitch.draw(figsize=(16,11))
    ax_title = ax.set_title(f'{player} Succesful ball recoveries', fontsize = 30)
    fig.set_facecolor('white')
    if len(player_br) == 0:
        return fig
    
    else:
        player_br[['x', 'y']] = player_br['location'].apply(pd.Series)
        # drawing ball recoveries location
        pitch.scatter(player_br.x, player_br.y, color = 'red',s =200 ,marker="o", ax = ax, zorder = 2, label = "Ball Recovery")
        return fig
    
chosen_player = st.selectbox("Players:", players)
status = st.selectbox("Aspects :", ['Pass', 'Recovery'])

if status == 'Pass':
    st.pyplot(pass_visualization(chosen_player))

if status == 'Recovery':        
    st.pyplot(ball_recovery_visualization(chosen_player))
