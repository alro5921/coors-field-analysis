import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import retrosheet_pipeline as rs_pl

#MINUS WAS
TEAM_CODES = ['SLN', 'MIN', 'CLE', 'CHA', 'TOR', 'TEX', 'ANA', 'BAL', 'SFN',
       'PIT', 'SDN', 'ATL', 'COL', 'BOS', 'NYN', 'KCA', 'DET', 'SEA',
       'HOU', 'LAN', 'CHN', 'TBA', 'NYA', 'OAK', 'MIA', 'CIN',
       'PHI', 'ARI', 'MIL']

def season_half_win_rates(team_df):
    first_half_months = [4,5,6]
    second_half_months = [7,8,9]
    first_half = team_df[team_df.date.dt.month.isin(first_half_months)]
    second_half = team_df[team_df.date.dt.month.isin(second_half_months)]
    return first_half.mean(), second_half.mean()


def home_road_win_ratio(team_df):
    gb_home = team_df.groupby('home')
    gb_means = gb_home.mean()
    rat = gb_means.loc[True,'win']/gb_means.loc[False, 'win']
    return rat

def home_road_win_corr(team_df):
    gb_home_month = team_df.groupby([team_df.home, team_df.date.dt.month])
    mean_gb = gb_home_month.mean()
    monthly_avg_win = pd.DataFrame()
    #Excluding March and October
    #Which typically have 2-3 games and throw this off
    monthly_avg_win['home'] = mean_gb['win'][True][[4,5,6,7,8,9]]
    monthly_avg_win['away'] = mean_gb['win'][False][[4,5,6,7,8,9]]
    corr = monthly_avg_win.corr()
    return corr['home']['away']

def league_home_road_ratios(y_start, y_end, team_names):
    ratio_arr = []
    for team in team_names:
        team_df = rs_pl.team_data_pipeline(y_start, y_end, team)
        ratio_arr.append([team, home_road_win_ratio(team_df)])
    return ratio_arr

def trip_win_rates(team_df):
    gb_trip_length = team_df.groupby(team_df.game_in_trip)
    return gb_trip_length.mean()['win']

if __name__ == '__main__':
    
    test = False
    if test:
        league_home_road = league_home_road_ratios(2000,2019, TEAM_CODES)
        print(league_home_road)
        league_home_road.sort(key = lambda p: p[1], reverse = True)
        X = [point[0] for point in league_home_road]
        Y = [point[1] for point in league_home_road]
        
        plt.figure(figsize=(20,12))
        plt.style.use('ggplot')
        plt.xticks(rotation=60, size = 20)
        plt.yticks(size = 20)
        plt.title("Team Home Win/Away Win ratio from 2000-2019", size = 30)
        plt.ylabel("Home/Away Win Ratio", size = 20)
        colors = ['purple' if team == 'COL' else 'gray' for team in X]
        plt.bar(X, Y, color = colors)
        plt.ylim(1,1.5)
        plt.show()
    col_15_19 = rs_pl.team_data_pipeline(2000,2019,'COL')
    away = col_15_19[col_15_19.home]
    season_half_win_rates(away)
    trip_win_rates(away)