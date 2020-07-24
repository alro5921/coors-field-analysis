import pandas as pd
import numpy as np
from constants import TEAM_CODES

'''
The information used here was obtained free of
charge from and is copyrighted by Retrosheet.  Interested
parties may contact Retrosheet at "www.retrosheet.org".
'''

class SeasonalRetrosheetData:
    '''Fetches and processes retrosheet data on a seasonal (year by year) level, outputting either the cleaned dataframes
    or a team-specific data processors (TeamRetrosheetData class)
    '''
    def __init__(self, years):
        self.year_dfs = {}
        self.add_years(years)

    def get_retrosheet_season(self, year):
        '''Wrapper for getting grabbing the retrosheet data'''
        local_path = f'../data/rs_gamelogs/GL{year}.TXT' 
        try:
            df = pd.read_csv(local_path, header = None)
        except FileNotFoundError:
            df = pd.DataFrame([])
            print(f'Retrosheet for {year} not found locally, fetching from retrosheet...')
            rs_path = f'https://www.retrosheet.org/gamelogs/gl{year}.zip' 
            df = pd.read_csv(rs_path, header = None)
            df.to_csv(local_path)
        return df

    def clean_retrosheet_df(self, retro_df):
        cleaned_df = retro_df[[0,3,6,9,10]].copy()
        cleaned_df.columns = ["date", "away_team", "home_team", "away_score", "home_score"]
        cleaned_df["home_win"] = cleaned_df["home_score"] > cleaned_df["away_score"]
        cleaned_df["date"] = pd.to_datetime(cleaned_df["date"], format='%Y%m%d')
        return cleaned_df

    def add_years(self, years, overwrite = False):
        for year in years:
            if year not in self.year_dfs or overwrite:
                retro_df = self.get_retrosheet_season(year)
                self.year_dfs[year] = self.clean_retrosheet_df(retro_df)

    def get_years_in_data(self):
        return list(self.year_dfs.keys())

    def get_years_seperate(self):
        '''Returns all the seperate year dataframes instead of combining them'''
        return self.year_dfs

    def get_years(self, years):
        return pd.concat([self.year_dfs[year] for year in years]).reset_index(drop = True)

    def get_all(self, years = None):
        return self.get_years(self.get_years_in_data())

    def get_team_rs_data(self, team_codes = None):
        if not team_codes:
            team_codes = TEAM_CODES
        elif isinstance(team_codes, str):
            return TeamRetrosheetData(team_codes, self)
        return {team : TeamRetrosheetData(team, self) for team in team_codes}

class TeamRetrosheetData:
    '''Extracts and processes team-specific info from a Seasonal class'''

    def __init__(self, team_code, seasonal_rs_data):
        self.team_code = team_code.upper()
        self.year_dfs = {}
        self.seasonal_rs_data = seasonal_rs_data
        self.add_seasonal_rs_data(seasonal_rs_data)

    def pipeline(self, seasonal_rs_data, team_code):
        '''Calls all the transformation pipelines on the data'''
        team_df = self._to_team_data_pipeline(seasonal_rs_data, team_code)
        team_df = self._trip_lengths_pipeline(team_df)
        return team_df

    def _to_team_data_pipeline(self, df, team_code):
        '''Converts league-wide seasonal data into team specific data, grabbing relevant fields''' 
        team_df = df[(df['away_team'] == team_code) | (df['home_team'] == team_code)].copy()
        team_df.loc[:,'home'] = team_df['home_team'] == team_code
        team_df.loc[:,'win'] = ~(team_df['home'] ^ team_df['home_win'])
        team_df.loc[:,'score'] = team_df['home_score'].where(team_df['home'],team_df['away_score'])
        team_df.loc[:,'opponent'] = team_df['away_team'].where(team_df['home'],team_df['home_team'])
        team_df = team_df.reset_index()
        team_df['game_in_season'] = team_df.index
        return team_df[['game_in_season', 'date', 'home', 'opponent', 'score', 'win']]

    def _trip_lengths_pipeline(self, team_df):
        '''Adds the 'game_in_trip' column, how long (in games) the team had been on a home/road trip''' 
        ret_df = team_df
        ret_df['game_in_trip'] = 1
        is_home = True
        length = 0
        #I cry, but I don't see a way to vectorize this?
        for i in range(len(team_df)):
            if is_home != ret_df.loc[i,'home']:
                length = 0
                is_home = ret_df.loc[i,'home']
            length += 1    
            ret_df.loc[i,'game_in_trip'] = length
        return ret_df
        
    def add_seasonal_rs_data(self, seasonal_rs_data, overwrite = False):
        '''Constructs additional team data from more seasonal data'''
        for year in seasonal_rs_data.get_years_in_data():
            if year not in self.year_dfs or overwrite:
                self.year_dfs[year] = self.pipeline(seasonal_rs_data.get_years([year]), self.team_code)

    def add_years(self, years, overwrite = False):
        self.seasonal_rs_data.add_years(years, overwrite)
        self.add_seasonal_rs_data(self.seasonal_rs_data, overwrite)

    def get_years_in_data(self):
        return self.year_dfs.keys()

    def get_years_seperate(self):
        return self.year_dfs

    def get_years(self, years):
        return pd.concat([self.year_dfs[year] for year in years]).reset_index(drop = True)

    def get_all(self):
        return self.get_years(self.get_years_in_data())


if __name__ == '__main__':
    years = list(range(2015,2019 + 1))
    seasons_15_19 = SeasonalRetrosheetData(years)
    agg = seasons_15_19.get_all()
    lan_rs_data = TeamRetrosheetData('LAN', seasons_15_19)
    agg_lan = lan_rs_data.get_all()

