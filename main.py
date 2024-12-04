
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

# function visualization
def pass_visualization(player):
    player_passes = event[(event.player == player) & (event.type == "Pass") & (event.pass_outcome.isna())] #gettign data about passes
    player_passes[['x', 'y']] = player_passes['location'].apply(pd.Series) #divide location of event to two separete columns
    player_passes[['pass_end_x', 'pass_end_y']] = player_passes['pass_end_location'].apply(pd.Series) #divide end location pf event to separete columns
    
    # creting pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2,line_color='black') 
    fig, ax = pitch.draw(figsize=(16,11))
    fig.set_facecolor('white')
    
    # drawing passes
    pitch.arrows(player_passes.x, player_passes.y, player_passes.pass_end_x, player_passes.pass_end_y,
                width=3, headwidth=8, headlength=5, color = 'green', ax = ax, zorder = 2, label = "Pass")
    ax_title = ax.set_title(f'{player} passes', fontsize = 30) #drawing arrows using data about events locations
    return ax

pass_visualization('Granit Xhaka')
plt.show()