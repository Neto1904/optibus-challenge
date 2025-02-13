import pandas as pd  
from datetime import timedelta
import json

def read_dataset(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def create_normalized_dataframe(dataset, key, id_column, list_column):
    normalized_df = pd.json_normalize(dataset[key], list_column, id_column)
    return normalized_df

def create_dataframe(dataset, key):
    df = pd.DataFrame(dataset[key])
    return df

def join_dataframes(df1, df2, key):
    df1[key] = df1[key].astype(int)
    df2[key] = df2[key].astype(int)
    return pd.merge(df1, df2, on=key, how='inner')

def concat_dataframes(df1, df2):
    return pd.concat([df1, df2], axis=0)

def split_dataframe(df, k):
    # Split the dataframe into k equal parts
    smaller_dfs = [df[i:i + k] for i in range(0, len(df), k)]
    return smaller_dfs