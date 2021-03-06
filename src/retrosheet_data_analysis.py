import pandas as pd
import numpy as np
import scipy.stats as stats

from retrosheet_pipeline import SeasonalRetrosheetData, TeamRetrosheetData
from constants import TEAM_CODES, MONTH_DICT

def home_road_monthly_winrate(team_df, remove_march_oct = True):
    team_gb_h_month = team_df.groupby([team_df.home, team_df.date.dt.month])
    gb_mean = team_gb_h_month.mean()
    y = pd.DataFrame()
    y['Home'] = gb_mean['win'][True]
    y['Away'] = gb_mean['win'][False]
    y = y.drop(3, errors = 'ignore').drop(10, errors = 'ignore')
    return y

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
    #Cutting off March and October, which typically have 1-2 games per season
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

def trip_scores(team_df):
    gb_trip_length = team_df.groupby([team_df.home, team_df.game_in_trip])
    return gb_trip_length.mean()['score'][True], gb_trip_length.mean()['score'][False]

def from_coors_trip_scores(team_df):
    gb_gfcoors = team_df.groupby([team_df.game_from_coors])
    games_out = 8 #Games out
    game_range = list(range(1,games_out + 1))
    return gb_gfcoors.mean()['win'][game_range] ,gb_gfcoors.count()['win'][game_range]

if __name__ == '__main__':
    years = list(range(2002,2019 + 1))
    seasons_02_19 = SeasonalRetrosheetData(years)
    team_rs_data = seasons_02_19.get_team_rs_data()
    col_rs_data = team_rs_data['COL']

    #Calculate chi squared tests
    col_rs_data = TeamRetrosheetData('COL', seasons_02_19).get_all()
    col_gb_h_month = col_rs_data.groupby([col_rs_data.home,col_rs_data.date.dt.month])
    wins = col_gb_h_month.sum()['win'][False].drop(10)
    total = col_gb_h_month.count()['win'][False].drop(10)
    losses = total - wins
    contig_table = np.array([list(wins), list(losses)])
    print(stats.chi2_contingency(contig_table))


