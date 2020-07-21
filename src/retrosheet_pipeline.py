import pandas as pd
import numpy as np

class SeasonalRetrosheetData:
    
    def __init__(self, years):
        self.year_dfs = {}
        self.add_years(years)
        self.pipeline = []

    def get_years(self):
        return self.year_dfs.keys()

    def add_years(self, years, overwrite = False):
        for year in years:
            if year not in self.year_dfs or overwrite:
                retro_df = get_retrosheet_season(year)
                self.year_dfs[year] = self.clean_retrosheet_df(retro_df)

    def clean_retrosheet_df(self, retro_df):
        retro_df = retro_df[[0,3,6,9,10]]
        retro_df.columns = ["date", "away_team", "home_team", "away_score", "home_score"]
        retro_df.loc[:,"home_win"] = retro_df["home_score"] > retro_df["away_score"]
        retro_df.loc[:, "date"] = pd.to_datetime(retro_df["date"], format='%Y%m%d')
        return retro_df.copy()

    def get_df_dict(self):
        return self.year_dfs

    def get_year_df(self, year):
        if not year in self.year_dfs:
            return None
        return self.year_dfs[year]

    def get_aggregate_df(self, years = None):
        if not years:
            years = self.get_years()
        return pd.concat([self.year_dfs[year] for year in years])

class TeamRetrosheetData:

    def __init__(self, team_code, years = None, seasonal_rs_data = None):
        self.team_code = team_code
        self.year_dfs = {}
        self.seasonal_rs_data = None
        if seasonal_rs_data:
            self.seasonal_rs_data = seasonal_rs_data
        elif years:
            self.seasonal_rs_data = SeasonalRetrosheetData(years)
        self.add_seasonal_rs_data(seasonal_rs_data)

    def add_seasonal_rs_data(self, seasonal_rs_data, overwrite = False):
        for year in seasonal_rs_data.get_years():
            if year not in self.year_dfs or overwrite:
                self.year_dfs[year] = self.to_team_data_pipeline(seasonal_rs_data.get_year_df(year), self.team_code)

    #def _update_seasonal_rs_data_pipe

    def get_years(self):
        return self.year_dfs.keys()

    def add_years(self, years, overwrite = False):
        self.seasonal_rs_data.add_years(years, overwrite)
        self.add_seasonal_rs_data(seasonal_rs_data, overwrite)

    def to_team_data_pipeline(self, df, team_code):
        team_df = df[(df['away_team'] == team_code) | (df['home_team'] == team_code)]
        team_df.loc[:,'home'] = team_df['home_team'] == team_code
        team_df.loc[:,'win'] = ~(team_df['home'] ^ team_df['home_win'])
        team_df.loc[:,'score'] = team_df['home_score'].where(team_df['home'],team_df['away_score'])
        team_df = team_df.reset_index()
        self.add_trip_lengths(team_df)
        return team_df[['date', 'home', 'score', 'win']]

    def add_trip_lengths(self, team_df):
        ret_df = team_df
        ret_df['game_in_trip'] = 1
        is_home = True
        length = 0
        for i in range(len(team_df)): #I cry, but I don't see a way to vectorize this?
            if is_home != ret_df.loc[i,'home']:
                length = 0
                is_home = ret_df.loc[i,'home']
            length += 1    
            ret_df.loc[i,'game_in_trip'] = length
        return ret_df[['date', 'home', 'game_in_trip', 'win', 'score']]

    def get_year_df(self, year):
        return self.year_dfs.keys()

    def get_aggregate_df(self, years = None):
        if not years:
            years = self.get_years()
        return pd.concat([self.year_dfs[year] for year in years])

#Wrapper for "If file local, grab that, else grab from retrosheet and put it into local."
def get_retrosheet_season(year):
    local_path = f'../data/rs_gamelogs/GL{year}.TXT' 
    try:
        df = pd.read_csv(local_path, header = None)
    except FileNotFoundError:
        print(f'Retrosheet for {year} not found locally, fetching from retrosheet...')
        rs_path = f'https://www.retrosheet.org/gamelogs/gl{year}.zip' 
        df = pd.read_csv(rs_path, header = None)
        df.to_csv(local_path)
    return df

# #Discards a LOT of extraneous retrosheet data, cleans remaining data up somewhat, and add headers to the columns
# #Meaning of the retrosheet columns are documented at https://www.retrosheet.org/gamelogs/glfields.txt
# def clean_retrosheet_df(retro_df):
#     retro_df = retro_df[[0,3,6,9,10]]
#     retro_df.columns = ["date", "away_team", "home_team", "away_score", "home_score"]
#     retro_df.loc[:,"home_win"] = retro_df["home_score"] > retro_df["away_score"]
#     retro_df.loc[:, "date"] = pd.to_datetime(retro_df["date"], format='%Y%m%d')
#     return retro_df.copy()

# #Extracts a particular team's season data (and rearranges data to make sense).
# def to_team_data(df, team_code):
#     team_df = df[(df['away_team'] == team_code) | (df['home_team'] == team_code)]
#     team_df.loc[:,'home'] = team_df['home_team'] == team_code
#     team_df.loc[:,'win'] = ~(team_df['home'] ^ team_df['home_win'])
#     team_df.loc[:,'score'] = team_df['home_score'].where(team_df['home'],team_df['away_score'])
#     team_df = team_df.reset_index()
#     return team_df[['date', 'home', 'score', 'win']]

# #Adds how long the team has been on a particular trip (home or away) in each game.
# #First game on road = 1, second game on road = 2, and so forth.
# def add_trip_lengths(team_df):
#     ret_df = team_df
#     ret_df['game_in_trip'] = 1
#     is_home = True
#     length = 0
#     for i in range(len(team_df)): #I cry, but I don't see a way to vectorize this?
#         if is_home != ret_df.loc[i,'home']:
#             length = 0
#             is_home = ret_df.loc[i,'home']
#         length += 1    
#         ret_df.loc[i,'game_in_trip'] = length
#     return ret_df[['date', 'home', 'game_in_trip', 'win', 'score']]

# #The whole shebang applied to multiple years
# def team_data_pipeline(y_start, y_end, team_code):
#     year_df_list = []
#     for year in range(y_start, y_end + 1):
#         retro_df = get_retrosheet_season(year)
#         df = clean_retrosheet_df(retro_df)
#         df = to_team_data(df, team_code)
#         df = add_trip_lengths(df)
#         year_df_list.append(df)
#     agg_df = pd.concat(year_df_list)
#     return agg_df

if __name__ == '__main__':
    years = list(range(2002,2020))
    seasons_02_19 = SeasonalRetrosheetData(years)
    print(seasons_02_19.get_year_df(2003).head(20))
    #col_15_19 = team_data_pipeline(2015,2019,'COL')
    #print(col_15_19.head()) 
    #gb_home = col_15_19.groupby('home')
    #print(gb_home.mean()) 
