import pandas as pd

#Save a pandas DataFrame as an encoded csv file
def df_to_csv (df, path, sep =',', encoding='utf-8'):
    df.to_csv(path, sep = sep, encoding = encoding)

#Save a pandas DataFrame as a json file    
def df_to_json (df, path, orient):
    df.to_json(path, orient = orient)