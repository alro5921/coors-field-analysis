import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# activate latex text rendering
import retrosheet_data_analysis
from retrosheet_pipeline import SeasonalRetrosheetData, TeamRetrosheetData

plt.style.use('ggplot')

TEAM_CODES = ['SLN', 'MIN', 'CLE', 'CHA', 'TOR', 'TEX', 'ANA', 'BAL', 'SFN',
       'PIT', 'SDN', 'ATL', 'COL', 'BOS', 'NYN', 'KCA', 'DET', 'SEA',
       'HOU', 'LAN', 'CHN', 'TBA', 'NYA', 'OAK', 'MIA', 'CIN',
       'PHI', 'ARI', 'MIL']

def save_image(name, folder_path = '../images'):
    file_path = folder_path + f'/{name}.png'
    plt.savefig(file_path)

def set_style(ax):
    pass

def bold_COL_label(labels):
    return ["{coo"]

def grouped_bar_frame(ax, vals, group_names, legend_names):
    '''Plots framework for a grouped bar plot (to be fine tuned in the scope above)'''

    width = .2
    ind = np.arange(len(vals))
    arr = np.array(vals)
    ax.bar(ind - width/2, arr[:,0], width, label = legend_names[0])
    ax.bar(ind + width/2, arr[:,1], width, label = legend_names[1])
    ax.set_xticks(ind)
    ax.set_xticklabels(group_names)
    ax.legend(prop=dict(size=18))
    #for i in range(ind):
    #ind_vals = arr[:,i]

def league_one_bar_frame(ax, team_list, data, title, ylabel):
    '''Plots framework for a simple league-wide comparison bar graph)'''
    ax.tick_params(axis='x', rotation=45, labelsize = 20)
    ax.tick_params(axis='y', labelsize = 20)
    ax.set_title(title, size = 30)
    ax.set_ylabel(ylabel, size = 20)
    colors = ['purple' if team == 'COL' else 'gray' for team in team_list]
    ax.bar(team_list, data, color = colors)

def month_line_frame(ax, data, title, ylabel):
    month_labels = ["April", "May", "June", 
                    "July", "August", "September"]


def create_ha_ratio(ax, seasonal_rs, team_codes = TEAM_CODES):
    league_home_road = retrosheet_data_analysis.league_home_road_ratios(seasonal_rs, team_codes)
    league_home_road.sort(key = lambda p: p[1], reverse = True)
    X = [point[0] for point in league_home_road]
    Y = [point[1] for point in league_home_road]
    
    title = "Team Home/Away Winrate Ratio from 2002-2019"
    ylabel = "Home/Away Win Ratio"
    league_one_bar_frame(ax, X, Y, title, ylabel)
    ax.set_ylim(1,1.5)

def create_halfs_chart(ax, team_df):
    home, away = team_df[team_df.home],team_df[~team_df.home]
    away_d, home_d = (retrosheet_data_analysis.season_half_win_rates(away),
                    retrosheet_data_analysis.season_half_win_rates(home) )
    grouped_bar_frame(ax, [home_d,away_d], ["Home", "Away"], ["First Half", "Second Half"])
    
    ax.set_ylim(0,.6)
    ax.set_yticks(np.arange(0, .6, step=0.1))
    ax.tick_params(axis = 'both', labelsize = 20)
    ax.set_ylabel("Winrate", size = 16)
    ax.set_title("First Half vs Second Half Winrates", size = 30)

#Not to be confused with coooooors
def create_corrs(ax,seasonal_rs, team_codes = TEAM_CODES):
    league_home_road_corrs = retrosheet_data_analysis.league_monthly_corrs(seasonal_rs, team_codes)
    league_home_road_corrs.sort(key = lambda p: p[1], reverse = True)
    X = [point[0] for point in league_home_road_corrs]
    Y = [point[1] for point in league_home_road_corrs]
    title = "Correlations of Monthly Home Win% to Away Win%"
    ylabel = "Correlation"
    league_one_bar_frame(ax, X, Y, title, ylabel)
    # rects = ax.patches
    # labels = X
    # for rect, label in zip(rects, labels):
    #     height = rect.get_height()
    #     ax.text(rect.get_x() + rect.get_width() / 2, height + .03, label,
    #     ha='center', va='bottom')
    ax.axhline(y = 0, color = 'k', linestyle = "--")
    ax.set_ylim(-1,1)

if __name__ == '__main__':
    years = list(range(2000,2020))
    seasons_02_19 = SeasonalRetrosheetData(years)
    col_rs_data = TeamRetrosheetData('COL', seasons_02_19)
    test1 = False
    if test1:
        #seasons_15_19 = seasons_02_19.get_years(list(range(2002,2020)))
        fig, ax = plt.subplots(figsize=(20,12))
        create_ha_ratio(ax, seasons_02_19)
        save_image("wl_ratio")
    test2 = False
    if test2:
        col_15_19 = col_rs_data.get_years(list(range(2002,2020)))
        fig, ax = plt.subplots(figsize=(10,10))
        create_halfs_chart(ax, col_15_19)
        save_image("halves")
    test3 = True
    if test3:
        fig, ax = plt.subplots(figsize=(20,12))
        create_corrs(ax, seasons_02_19)
        save_image("monthly_corrs")

