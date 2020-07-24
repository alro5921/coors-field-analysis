import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

import retrosheet_data_analysis
from retrosheet_pipeline import SeasonalRetrosheetData, TeamRetrosheetData
from constants import TEAM_CODES

plt.style.use('ggplot')

def save_image(name, folder_path = '../images'):
    file_path = folder_path + f'/{name}.png'
    plt.savefig(file_path)

def grouped_bar_frame(ax, vals, group_names, legend_names, colors, width = .2):
    '''Plots framework for a grouped bar plot (to be fine tuned in the scope above)'''
    width = .2
    ind = np.arange(2)
    arr = np.array(vals)
    ax.bar(ind - width/2, arr[:,0], width, label = legend_names[0], color = colors[0])
    ax.bar(ind + width/2, arr[:,1], width, label = legend_names[1], color = colors[1])
    ax.set_xticks(ind)
    ax.set_xticklabels(group_names)
    ax.legend(prop=dict(size=18))

def league_one_bar_frame(ax, team_list, data, title, ylabel):
    '''Plots framework for a simple league-wide comparison bar graph)'''
    ax.tick_params(axis='x', rotation=45, labelsize = 20)
    ax.tick_params(axis='y', labelsize = 20)
    ax.set_title(title, size = 30)
    ax.set_ylabel(ylabel, size = 20)
    colors = ['purple' if team == 'COL' else 'gray' for team in team_list]
    ax.bar(team_list, data, color = colors)

def line_frame(ax, data, x_labels = None, color = 'purple', label = ''):
    '''Plots framework for a line graph'''
    if not x_labels:
        x_labels = np.arange(1,len(data) + 1)
    ax.scatter(x_labels, data, color = color, label = label, s = 90)
    ax.plot(x_labels, data, color = color, 
            linestyle = "--", alpha = .3)

def month_line_frame(ax, data, color = 'purple', label = ''):
    month_labels = ["April", "May", "June", 
                    "July", "August", "September"]
    line_frame(ax, data, month_labels, color = color, label = label)

def create_trip_fall_off(ax, data):
    _, away_data = retrosheet_data_analysis.trip_scores(data)
    away_data = away_data[:8]
    X = np.arange(1,len(away_data) + 1)
    m, b = np.polyfit(X, np.array(away_data), 1)
    fit_line = lambda x: m*x + b

    ax.scatter(X, away_data, color = 'purple')
    ax.plot(X, away_data, color = 'purple', 
            linestyle = "--", alpha = .3)
    ax.plot(X, fit_line(X), linestyle = "-", alpha = .8, color = 'k', label = f'Fit, \nb = {b:.3f},\n m = {m:.3f}')

    ax.tick_params(axis = 'both', labelsize = 15)
    ax.set_ylabel("Runs Scored", size = 20)
    ax.set_ylim(3.75, 4.25)
    ax.set_yticks(np.arange(3.75, 4.30, step=0.05))
    ax.set_title("Average Runs Scored In Xth Game Of Road Trip", size = 20)
    ax.legend(fontsize = 15)

def create_monthly_win_rate(ax, y):
    month_line_frame(ax,y['Away'], color = '#348ABD', label = 'Away')
    month_line_frame(ax,y['Home'], color = '#E24A33', label = 'Home')
    
    ax.axhline(y = .5, color = 'k', linestyle = "--")
    ax.legend(fontsize = 15, loc = 'lower right')
    ax.tick_params(axis = 'both', labelsize = 15)
    ax.set_ylabel("Winrate", size = 30)
    ax.set_title("Rockies Winrate by Month", size = 30)

def create_home_away_ratio(ax, seasonal_rs, team_codes = TEAM_CODES):
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
    grouped_bar_frame(ax, [home_d,away_d], ["Home", "Away"], ["First Half", "Second Half"], colors = ['#13866d', '#ba8f0d'])
    
    ax.set_ylim(0,.6)
    ax.set_yticks(np.arange(0, .6, step=0.125))
    ax.tick_params(axis = 'both', labelsize = 20)
    ax.set_ylabel("Winrate", size = 16)
    ax.set_title("First Half vs Second Half Winrates", size = 30)

def create_corrs(ax,seasonal_rs, team_codes = TEAM_CODES):
    league_home_road_corrs = retrosheet_data_analysis.league_monthly_corrs(seasonal_rs, team_codes)
    league_home_road_corrs.sort(key = lambda p: p[1], reverse = True)
    X = [point[0] for point in league_home_road_corrs]
    Y = [point[1] for point in league_home_road_corrs]
    title = "Correlations of Monthly Home Win% to Away Win%"
    ylabel = "Correlation"
    league_one_bar_frame(ax, X, Y, title, ylabel)
    ax.axhline(y = 0, color = 'k', linestyle = "--")
    ax.set_ylim(-1,1)


if __name__ == '__main__':
    years = list(range(2002,2020))
    seasons_02_19 = SeasonalRetrosheetData(years)
    col_rs_data = TeamRetrosheetData('COL', seasons_02_19)

    generate_wl = False
    if generate_wl:
        fig, ax = plt.subplots(figsize=(20,12))
        create_home_away_ratio(ax, seasons_02_19)
        save_image("wl_ratio")

    generate_halves = False
    if generate_halves:
        col_15_19 = col_rs_data.get_years(list(range(2002,2020)))
        fig, ax = plt.subplots(figsize=(10,10))
        create_halfs_chart(ax, col_15_19)
        save_image("halves")

    generate_m_winrates = True
    if generate_m_winrates:
        fig, ax = plt.subplots(figsize=(10,10))
        col_all = col_rs_data.get_all()
        y = retrosheet_data_analysis.home_road_monthly_winrate(col_all)
        create_monthly_win_rate(ax, y)
        save_image("monthly_winrates")

    generate_corrs = False
    if generate_corrs:
        fig, ax = plt.subplots(figsize=(20,12))
        create_corrs(ax, seasons_02_19)
        save_image("monthly_corrs")


    generate_trip_winrates = False
    if generate_trip_winrates:
        fig, ax = plt.subplots(figsize=(12,10))
        col_all = col_rs_data.get_all()
        create_trip_fall_off(ax, col_rs_data.get_all())
        save_image("road_trip_runs")

