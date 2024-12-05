
import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import streamlit as st

competitions = sb.competitions() # getting data of all avaible competitions

matches = sb.matches(competition_id = 9, season_id = 281) # getting matches from Bundesliga season

# getting list of games id
matches_id = list(matches['match_id'])

event = sb.events(match_id = 3895302) # geting event from specific game

# function for pass visualization
def pass_visualization(player):
    player_passes = event[(event.player == player) & (event.type == "Pass") & (event.pass_outcome.isna())]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2,line_color='black')
    fig, ax = pitch.draw(figsize=(16,11))
    ax_title = ax.set_title(f'{player} passes', fontsize = 30)
    fig.set_facecolor('white')
    if  len(player_passes) == 0:
        return ax
    else:
        player_passes[['x', 'y']] = player_passes['location'].apply(pd.Series)
        player_passes[['pass_end_x', 'pass_end_y']] = player_passes['pass_end_location'].apply(pd.Series)

        # drawing passes
        pitch.arrows(player_passes.x, player_passes.y, player_passes.pass_end_x, player_passes.pass_end_y,
                    width=3, headwidth=8, headlength=5, color = 'green', ax = ax, zorder = 2, label = "Pass")
        return ax

pass_visualization('Granit Xhaka')
plt.show()

# function for ball recovery visualization
def ball_recovery_visualization(player):
    player_br = event[(event.player == player) & (event.type == "Ball Recovery") & (event.ball_recovery_recovery_failure.isna())]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2,line_color='black')
    fig, ax = pitch.draw(figsize=(16,11))
    ax_title = ax.set_title(f'{player} Succesful ball recoveries', fontsize = 30)
    fig.set_facecolor('white')
    if len(player_br) == 0:
        return ax
    
    else:
        player_br[['x', 'y']] = player_br['location'].apply(pd.Series)
        # drawing ball recoveries location
        pitch.scatter(player_br.x, player_br.y, color = 'red',s =200 ,marker="o", ax = ax, zorder = 2, label = "Ball Recovery")
        return ax
    
ball_recovery_visualization('Jonathan Tah')
plt.show()

# function for won duels visualization
def won_duel_visualization(player):
    player_duel = event[(event.player == player) & (event.type == "Duel") & (event.duel_outcome == "Won")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2,line_color='black')
    fig, ax = pitch.draw(figsize=(16,11))
    ax_title = ax.set_title(f'{player} won duels', fontsize = 30)
    fig.set_facecolor('white')
    if len(player_duel) == 0: 
        return ax
    else:
        player_duel[['x', 'y']] = player_duel['location'].apply(pd.Series)    
        # drawing duel locations
        pitch.scatter(player_duel.x, player_duel.y, color = 'red',s =200 ,marker="o", ax = ax, zorder = 2, label = "Duel")
        return ax
    
won_duel_visualization('Granit Xhaka')
plt.show()