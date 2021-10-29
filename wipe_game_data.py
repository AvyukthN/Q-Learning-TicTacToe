import pandas as pd

df = pd.DataFrame({
    'id': 0,
    'winner': 0,
    'state-1': pd.Series([0]),
    'state-2': pd.Series([0]),
    'state-3': pd.Series([0]),
    'state-4': pd.Series([0]),
    'state-5': pd.Series([0]),
    'state-6': pd.Series([0]),
    'state-7': pd.Series([0]),
    'state-8': pd.Series([0]),
    'state-9': pd.Series([0]),
})

df.to_csv('./game_data/games.csv')