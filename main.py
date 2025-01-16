import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from matplotlib.backends.backend_pdf import PdfPages

st.write ("data provided by")
logofile = 'hudlstatsbomblogo.jpg' #setting required statsbomb logo 
st.image(logofile)

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
        duels_won = duels[(duels.duel_outcome == "Success In Play") | (duels.duel_outcome == "Won")
                          | (duels.duel_outcome == "Success") | (duels.duel_outcome == "Success Out")
                          | (duels.duel_outcome == "Success To Team") | (duels.duel_outcome == "Aerial Success")]
        duels_lost = duels[(duels.duel_outcome == "Lost In Play") | (duels.duel_outcome == "Lost")
                           | (duels.duel_outcome == "Lost Out") | (duels.duel_outcome == "Aerial Lost")]
        duels_lost_dispossessed = pd.concat([duels_lost, dispossessed], ignore_index=True, sort=False)

        if len(duels_won) > 0:
            duels_won[['x', 'y']] = duels_won['location'].apply(pd.Series)
            pitch.scatter(duels_won.x, duels_won.y, color='green', s=7, marker="o", ax=ax,
                          zorder=2, label="Duel won")
        if len(duels_lost_dispossessed) > 0:
            duels_lost_dispossessed[['x', 'y']] = duels_lost_dispossessed['location'].apply(pd.Series)
            pitch.scatter(duels_lost_dispossessed.x, duels_lost_dispossessed.y, color='red', s=7, marker="o", ax=ax,
                          zorder=2, label="Duel lost or dispossessed")
        # if len(dispossessed) > 0:
        #     dispossessed[['x', 'y']] = dispossessed['location'].apply(pd.Series)
        #     pitch.scatter(dispossessed.x, dispossessed.y, color='red', s=7, marker="o", ax=ax, zorder=2)

    ax.legend(loc='lower center', ncol=3, fontsize=7, bbox_to_anchor=(0.5, -0.05))

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

        passes_bad = passes[passes.pass_outcome.notna()]
        passes_good = passes[passes.pass_outcome.isna()]
        passes_assist = passes[passes.pass_goal_assist == True]

        # drawing passes
        pitch.arrows(passes_bad.x, passes_bad.y, passes_bad.pass_end_x, passes_bad.pass_end_y,
                     width=1, headwidth=4, headlength=3, color='red', ax=ax, zorder=2, label="Wrong pass")
        # drawing good passes
        pitch.arrows(passes_good.x, passes_good.y, passes_good.pass_end_x, passes_good.pass_end_y,
                     width=1, headwidth=4, headlength=3, color='black', ax=ax, zorder=2, label="Good pass")
        # drawing assist passes
        pitch.arrows(passes_assist.x, passes_assist.y, passes_assist.pass_end_x, passes_assist.pass_end_y,
                     width=1.5, headwidth=4, headlength=3, color='green', ax=ax, zorder=2, label="Assist")

    ax.legend(loc='lower center', ncol=3, fontsize=7, bbox_to_anchor=(0.5, -0.05))

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

    ax.legend(loc='lower center', ncol=2, fontsize=7, bbox_to_anchor=(0.5, -0.05))

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

    ax.legend(loc='lower center', ncol=3, fontsize=7, bbox_to_anchor=(0.5, -0.05))

    return


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

    fig.set_size_inches(7, 7)

    fig.tight_layout(h_pad=2, w_pad=0)
    plt.subplots_adjust(left=0.0, bottom=0.1, right=1.0, top=0.9, wspace=0.1, hspace=0.1)

    fig.set_facecolor('white')
    fig.suptitle(f'{player} game performance')

    if position == 'Goalkeeper':
        pass_pitch(axs[0], player)
        recovery_pitch(axs[1], player)
    else:
        pass_pitch(axs[0, 0], player)
        recovery_pitch(axs[0, 1], player)
        duel_pitch(axs[1, 0], player)
        shot_pitch(axs[1, 1], player)
        # empty_pitch(axs[2, 1])

    return fig


def creating_stat_table(player, position):
    # success rate of passes
    player_passes = event['pass_outcome'][
        (event.player == player) & (event.type == "Pass") & (event.pass_outcome != 'Unknown')]
    passes = str(round((1 - (player_passes.count() / len(player_passes))) * 100, 2)) + '%'
    # number of succesful ball recoveries
    player_r = event[(event.player == player) & (event.type == "Ball Recovery")]
    rec = player_r['ball_recovery_recovery_failure'].isna().count()
    if position == 'Goalkeeper':
        # number of shots saved and parried to opponent
        saved_op = len(event[(event.player == player) & (event.type == "Goal Keeper") & (
                    event.goalkeeper_type == "Shot Saved") & (event.goalkeeper_outcome == 'In Play Danger')])
        # number of shots saved and parried to a teammate
        saved_t = len(event[(event.player == player) & (event.type == "Goal Keeper") & (
                    event.goalkeeper_type == "Shot Saved") & (event.goalkeeper_outcome == 'In Play Safe')])
        # number of goals conceded
        conceded = len(event[(event.player == player) & (event.type == "Goal Keeper") & (
                    event.goalkeeper_type == "Goal Conceded")])
        # number of succesful punches
        punches = len(event[(event.player == player) & (event.type == "Goal Keeper") & (
                    event.goalkeeper_type == "Punches") & (event.goalkeeper_outcome == 'Sucess')])
        names1 = ['success rate of passes', 'succesfull ball recoveries', 'shots saved and parried to opponent']
        stats1 = [passes, rec, saved_op]
        names2 = ['shots saved and parried to a teammate', 'goals conceded', 'succesful punches']
        stats2 = [ saved_t, conceded, punches]
    else:
        # number of shots on target
        player_s = event[(event.player == player) & (event.type == "Shot")]
        shots = len(player_s[(player_s.shot_outcome == 'Saved') | (player_s.shot_outcome == 'Goal') | (
                    player_s.shot_outcome == 'Saved To Post')])
        # number of won duels
        player_r = event[(event.player == player) & (event.type == "Duel")]
        duels = len(player_r[(player_r.duel_outcome == 'Won') | (player_r.duel_outcome == 'Success In Play') |
                             (player_r.duel_outcome == 'Success') | (player_r.duel_outcome == 'Success Out') |
                             (player_r.duel_outcome == 'Success To Team') | (
                                         player_r.duel_outcome == 'Aerial Success')])
        # number of succesfull dribligns
        player_dr = event[(event.player == player) & (event.type == "Dribble")]
        drib = len(player_dr[(player_dr.dribble_outcome == 'Complete')])
        # number of ball losses
        los = len(event[(event.player == player) & (event.type == "Dispossessed")])
        # number of fauls commited
        fc = len(event[(event.player == player) & (event.type == "Foul Commited")])
        # number of fouls suffered
        fw = len(event[(event.player == player) & (event.type == "Foul Won")])
        names1 = ['success rate of passes', 'succesfull ball recoveries', 'shots on target', 'won duels']
        names2 = ['succesfull dribblings', 'ball losses', 'fouls commited', 'fouls won']

        stats1 = [passes, rec, shots, duels]
        stats2 = [ drib, los, fc, fw]
    df1 = pd.DataFrame(list(zip(names1, stats1)), columns=['Parameter', 'Value'])
    df2 = pd.DataFrame(list(zip(names2, stats2)), columns=['Parameter', 'Value'])
    return df1, df2


# defining position (goalkeeper or other position)
position = "?"
chosen_player = st.selectbox("Player:", players)  # players selectbox
player_position_list = event[(event.player == chosen_player)]['position'].unique()
if len(player_position_list) == 1:
    position = player_position_list[0]

st.header(f'{chosen_player} statistics')
stats = creating_stat_table(chosen_player, position)
df1 = stats[0].transpose()
df2 = stats[1].transpose()
st.table(df1.style.set_properties(**{'background-color': 'lightblue'}))
st.table(df2.style.set_properties(**{'background-color': 'lightblue'}))
st.pyplot(prepare_figure(chosen_player, position))

# creating button with on click
def drawBtn():
    st.button("Print to pdf", on_click= creating_pdf, use_container_width=True, type = 'primary')
   
# creating pdf with report
def creating_pdf():
    with PdfPages(f'{chosen_player} report.pdf') as pdf:
        fig, (ax1, ax2) = plt.subplots(2,1,figsize=(8,3))
        
        ax1.axis('off')
        ax2.axis('off')
        
    
        df1 = stats[0].transpose()
        df2 = stats[1].transpose()
        
        
        table1 = ax1.table(cellText = df1.values,
                          colLabels = df1.columns,
                          cellColours = [['lightblue']*len(df1.columns),
                                         ['lightblue']*len(df1.columns)],
                          loc = 'center')
    
        
        table2 = ax2.table(cellText = df2.values,
                          colLabels = df2.columns,
                          cellColours = [['lightblue']*len(df1.columns),
                                         ['lightblue']*len(df1.columns)],
                          loc = 'center')
        
        
        fig.suptitle("Player statistics")
        pdf.savefig()
        
        fig1 =  prepare_figure(chosen_player, position)
        fig1.show()
        
        pdf.savefig()
        
        
drawBtn()