import pandas as pd
import numpy as np

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

#Discards a LOT of extraneous retrosheet data, cleans remaining data up somewhat, and add headers to the columns
#Meaning of the retrosheet columns are documented at https://www.retrosheet.org/gamelogs/glfields.txt
def clean_retrosheet_df(retro_df):
    retro_df = retro_df[[0,3,6,9,10]]
    retro_df.columns = ["date", "away_team", "home_team", "away_score", "home_score"]
    retro_df.loc[:,"home_win"] = retro_df["home_score"] > retro_df["away_score"]
    retro_df.loc[:, "date"] = pd.to_datetime(retro_df["date"], format='%Y%m%d')
    return retro_df.copy()

#Extracts a particular team's season data (and rearranges data to make sense).
def to_team_data(df, team_code):
    team_df = df[(df['away_team'] == team_code) | (df['home_team'] == team_code)]
    team_df.loc[:,'home'] = team_df['home_team'] == team_code
    team_df.loc[:,'win'] = ~(team_df['home'] ^ team_df['home_win'])
    team_df.loc[:,'score'] = team_df['home_score'].where(team_df['home'],team_df['away_score'])
    team_df = team_df.reset_index()
    return team_df[['date', 'home', 'score', 'win']]

#Adds how long the team has been on a particular trip (home or away) in each game.
#First game on road = 1, second game on road = 2, and so forth.
def add_trip_lengths(team_df):
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

#The whole shebang applied to multiple years
def team_data_pipeline(y_start, y_end, team_code):
    year_df_list = []
    for year in range(y_start, y_end + 1):
        retro_df = get_retrosheet_season(year)
        df = clean_retrosheet_df(retro_df)
        df = to_team_data(df, team_code)
        df = add_trip_lengths(df)
        year_df_list.append(df)
    agg_df = pd.concat(year_df_list)
    return agg_df

if __name__ == '__main__':
    col_15_19 = team_data_pipeline(2015,2019,'COL')
    print(col_15_19.head()) 
    gb_home = col_15_19.groupby('home')
    print(gb_home.mean()) 
