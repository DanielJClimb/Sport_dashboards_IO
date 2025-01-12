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

players = list(event.player.unique())  # list of players for selectbox
players = [p for p in players if p == p]  # removing nan values

# function for dispossessed and duels visualization (dispossessed)
def dispossessed_pitch(ax, player):
    player_d = event[(event.player == player) & (event.type == "Dispossessed")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black', linewidth=1)
    pitch.draw(ax=ax, figsize=(16, 11))
    ax_title = ax.set_title('Dispossessed', fontsize=8)
    if len(player_d) > 0:
        player_d[['x', 'y']] = player_d['location'].apply(pd.Series)
        # drawing ball dispossessed location
        pitch.scatter(player_d.x, player_d.y, color='red', s=7, marker="o", ax=ax, zorder=2, label="Dispossessed")

    return

# function for disspossed and duels visualization (duels)
def duel_pitch(ax, player):
    duels = event[(event.player == player) & (event.type == "Duel")]
    dispossessed = event[(event.player == player) & (event.type == "Dispossessed")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black', linewidth=1)
    pitch.draw(ax=ax, figsize=(16, 11))
    ax_title = ax.set_title('Duels', fontsize=8)
    if len(duels) > 0:
        duels[['x', 'y']] = duels['location'].apply(pd.Series)
        # drawing duel locations
        pitch.scatter(duels.x, duels.y, color='red', s=7, marker="o", ax=ax, zorder=2, label="Duel")
        duels_won = duels[(duels.duel_outcome == "Success In Play") | (duels.duel_outcome == "Won")
                          | (duels.duel_outcome == "Success") | (duels.duel_outcome == "Success Out")
                          | (duels.duel_outcome == "Success To Team") | (duels.duel_outcome == "Aerial Success")]
        duels_lost = duels[(duels.duel_outcome == "Lost In Play") | (duels.duel_outcome == "Lost")
                           | (duels.duel_outcome == "Lost Out") | (duels.duel_outcome == "Aerial Lost")]

        if len(duels_won) > 0:
            duels_won[['x', 'y']] = duels_won['location'].apply(pd.Series)
            pitch.scatter(duels_won.x, duels_won.y, color='green', s=7, marker="o", ax=ax, zorder=2,
                          label="Duel won")
        if len(duels_lost) > 0:
            duels_lost[['x', 'y']] = duels_lost['location'].apply(pd.Series)
            pitch.scatter(duels_lost.x, duels_lost.y, color='red', s=7, marker="o", ax=ax, zorder=2,
                          label="Duel lost")
        if len(dispossessed) > 0:
            dispossessed[['x', 'y']] = dispossessed['location'].apply(pd.Series)
            pitch.scatter(dispossessed.x, dispossessed.y, color='red', s=7, marker="o", ax=ax, zorder=2,
                          label="Dispossessed")

    return


# function for pass visualization
def pass_pitch(ax, player):
    passes = event[(event.player == player) & (event.type == "Pass")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black', linewidth=1)
    pitch.draw(ax=ax, figsize=(16, 11))
    ax_title = ax.set_title('Passes', fontsize=8)
    if len(passes) > 0:
        passes[['x', 'y']] = passes['location'].apply(pd.Series)
        passes[['pass_end_x', 'pass_end_y']] = passes['pass_end_location'].apply(pd.Series)

        passes_good = passes[passes.pass_outcome.isna()]
        passes_assist = passes[passes.pass_goal_assist == True]

        # drawing passes
        pitch.arrows(passes.x, passes.y, passes.pass_end_x, passes.pass_end_y,
                     width=1, headwidth=4, headlength=3, color='red', ax=ax, zorder=2, label="Pass")
        # drawing good passes
        pitch.arrows(passes_good.x, passes_good.y, passes_good.pass_end_x, passes_good.pass_end_y,
                     width=1, headwidth=4, headlength=3, color='black', ax=ax, zorder=2, label="Pass")
        # drawing assist passes
        pitch.arrows(passes_assist.x, passes_assist.y, passes_assist.pass_end_x, passes_assist.pass_end_y,
                     width=1.5, headwidth=4, headlength=3, color='green', ax=ax, zorder=2, label="Assist")

    ax.legend(labelspacing=1)
    plt.legend(loc='lower center', ncol=3, fontsize=7, bbox_to_anchor=(0.5, -0.05))

    return

# function for recovery visualization
def recovery_pitch(ax, player):
    recoveries = event[(event.player == player) & (event.type == "Ball Recovery")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black', linewidth=1)
    pitch.draw(ax=ax, figsize=(16, 16))
    ax_title = ax.set_title('Ball recoveries', fontsize=8)
    if len(recoveries) > 0:
        recoveries[['x', 'y']] = recoveries['location'].apply(pd.Series)
        # drawing duel locations
        # pitch.scatter(recoveries.x, recoveries.y, color='red', s=7, marker="o", ax=ax, zorder=2, label="Recovery")
        recoveries_won = recoveries[(recoveries.ball_recovery_recovery_failure.isna())]
        recoveries_lost = recoveries[(recoveries.ball_recovery_recovery_failure == "True")]

        if len(recoveries_won) > 0:
            recoveries_won[['x', 'y']] = recoveries_won['location'].apply(pd.Series)
            pitch.scatter(recoveries_won.x, recoveries_won.y, color='green', s=7, marker="o", ax=ax, zorder=2,
                          label="Recovery won")
        if len(recoveries_lost) > 0:
            recoveries_lost[['x', 'y']] = recoveries_lost['location'].apply(pd.Series)
            pitch.scatter(recoveries_lost.x, recoveries_lost.y, color='green', s=7, marker="o", ax=ax, zorder=2,
                          label="Recovery failed")

    ax.legend(labelspacing=1)
    plt.legend(loc='lower center', ncol=2, fontsize=7, bbox_to_anchor=(0.5, -0.05))

    return

# function for shot visualization
def shot_pitch(ax, player):
    shots = event[(event.player == player) & (event.type == "Shot")]
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black', linewidth=1)
    pitch.draw(ax=ax, figsize=(16, 16))
    ax_title = ax.set_title('Shots', fontsize=8)
    if len(shots) > 0:
        shots[['x', 'y']] = shots['location'].apply(pd.Series)
        shots_goal = shots[(shots.shot_outcome == "Goal")]
        shots_on = shots[(shots.shot_outcome == "Saved")]
        shots_off = shots[(shots.shot_outcome == "Post") |
                          (shots.shot_outcome == "Off T")]
        if len(shots_on) > 0:
            shots_on[['shot_end_x', 'shot_end_y', 'shot_end_z']] = shots_on['shot_end_location'].apply(pd.Series)
            pitch.arrows(shots_on.x, shots_on.y, shots_on.shot_end_x, shots_on.shot_end_y,
                         width=1, headwidth=4, headlength=3, color='black', ax=ax, zorder=2, label="Shot on")
        if len(shots_off) > 0:
            shots_off[['shot_end_x', 'shot_end_y', 'shot_end_z']] = shots_off['shot_end_location'].apply(pd.Series)
            pitch.arrows(shots_off.x, shots_off.y, shots_off.shot_end_x, shots_off.shot_end_y,
                         width=1, headwidth=4, headlength=3, color='red', ax=ax, zorder=2, label="Shot off")
        if len(shots_goal) > 0:
            shots_goal[['shot_end_x', 'shot_end_y', 'shot_end_z']] = shots['shot_end_location'].apply(pd.Series)
            pitch.arrows(shots_goal.x, shots_goal.y, shots_goal.shot_end_x, shots_goal.shot_end_y,
                         width=1, headwidth=4, headlength=3, color='green', ax=ax, zorder=2, label="Goal")

    ax.legend(labelspacing=1)
    plt.legend(loc='lower center', ncol=3, fontsize=7, bbox_to_anchor=(0.5, -0.05))

    return


    else:
        player_br[['x', 'y']] = player_br['location'].apply(pd.Series)
        # drawing ball recoveries location
        pitch.scatter(player_br.x, player_br.y, color='red', s=200, marker="o", ax=ax, zorder=2, label="Ball Recovery")
        return fig


# function for dispossessed visualization (for now not used)
def empty_pitch(ax):
    # creating pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black', linewidth=1)
    pitch.draw(ax=ax, figsize=(16, 11))

    return


def prepare_figure(player, position):
    if position == 'Goalkeeper':
        fig, axs = plt.subplots(1, 2)
    else:
        fig, axs = plt.subplots(2, 2)

    fig.set_size_inches(7,7)

    fig.tight_layout(h_pad=2, w_pad=0)
    plt.subplots_adjust(left=0.0, bottom=0.1, right=1.0, top=0.9, wspace=0.1, hspace=0.1)

    fig.set_facecolor('white')
    fig.suptitle(f'{player} statistics')

    if position == 'Goalkeeper':
        pass_pitch(axs[0], player)
        recovery_pitch(axs[1], player)
    else:
        pass_pitch(axs[0, 0], player)
        recovery_pitch(axs[0, 1], player)
        # dispossessed_pitch(axs[1, 0], player)
        duel_pitch(axs[1, 0], player)
        shot_pitch(axs[1, 1], player)
        # empty_pitch(axs[2, 1])

    return fig


#defining position (goalkeeper or other position)
position = "?"
chosen_player = st.selectbox("Players:", players)  # players selectbox
player_position_list = event[(event.player == chosen_player)]['position'].unique()
if len(player_position_list) == 1:
    position = player_position_list[0]

st.pyplot(prepare_figure(chosen_player, position))

# print(event)
