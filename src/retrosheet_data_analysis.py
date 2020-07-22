import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from retrosheet_pipeline import SeasonalRetrosheetData, TeamRetrosheetData

TEAM_CODES = ['SLN', 'MIN', 'CLE', 'CHA', 'TOR', 'TEX', 'ANA', 'BAL', 'SFN',
       'PIT', 'SDN', 'ATL', 'COL', 'BOS', 'NYN', 'KCA', 'DET', 'SEA',
       'HOU', 'LAN', 'CHN', 'TBA', 'NYA', 'OAK', 'MIA', 'CIN',
       'PHI', 'ARI', 'MIL']

def season_half_win_rates(team_df):
    is_half = team_df['game_in_season'] < 82
    first_half, second_half = team_df[is_half], team_df[~is_half]
    return first_half['win'].mean(), second_half['win'].mean()


def home_road_win_ratio(team_df):
    gb_home = team_df.groupby('home')
    gb_means = gb_home.mean()
    rat = gb_means.loc[True,'win']/gb_means.loc[False, 'win']
    return rat

def home_road_win_corr(team_df):
    gb_home_month = team_df.groupby([team_df.home, team_df.date.dt.month])
    mean_gb = gb_home_month.mean()
    monthly_avg_win = pd.DataFrame()
    #Excluding March and October, which typically have 1-2 games a SEASON
    monthly_avg_win['home'] = mean_gb['win'][True][[4,5,6,7,8,9]]
    monthly_avg_win['away'] = mean_gb['win'][False][[4,5,6,7,8,9]]
    corr = monthly_avg_win.corr()
    return corr['home']['away']

def league_monthly_corrs(seasonal_data, team_names):
    ratio_arr = []
    for team in team_names:
        team_df = TeamRetrosheetData(team, seasonal_rs_data=seasonal_data).get_all()
        ratio_arr.append([team, home_road_win_corr(team_df)])
    return ratio_arr

def league_home_road_ratios(seasonal_data, team_names):
    ratio_arr = []
    for team in team_names:
        team_df = TeamRetrosheetData(team, seasonal_rs_data=seasonal_data).get_all()
        ratio_arr.append([team, home_road_win_ratio(team_df)])
    return ratio_arr

def trip_win_rates(team_df):
    gb_trip_length = team_df.groupby(team_df.game_in_trip)
    return gb_trip_length.mean()['win']

if __name__ == '__main__':
    pass #Was formerly hosting all the graphing, should add simple tests when time