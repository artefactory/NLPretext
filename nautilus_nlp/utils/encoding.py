import pandas as pd
import chardet
import glob
import json

#Import an encoded csv or txt file as a pandas DataFrame
def import_from_file_as_pd(file, sep=',', header = None, verbose=True):
    encods = ['utf-8', 'ISO-8859-1', 'latin1', 'cp1252']
    try: 
        for encod in encods:
            try:
                data = pd.read_csv(file, sep = sep, encoding = encod, header=header)
                break
            except:
                continue
        if verbose:
            print('Success:',encod)
    except:
        rawdata = open(file, 'rb').read()
        result = chardet.detect(rawdata)['encoding']
        print(result)
        data = pd.read_csv(file, encoding = result, header=header)
    return data


#Import encoded csv or txt files from a folder as a pandas DataFrame
def import_from_folder_as_pd(path, sep = ',', verbose=False):
    all_files = glob.glob(path + "/*.csv")
    li = []
    
    for file in all_files:
        data = import_from_file_as_pd(file, sep = sep, verbose=verbose)
        li.append(data)
    
    frame = pd.concat(li, axis=0)
    return frame

#Import a json file as a pandas DataFrame
def import_json_to_pd(file):
    with open(file) as json_file:  
        data = json.load(json_file)
        json.dumps(data)
        df = pd.DataFrame(data)
    return df

#Import a json file as a dictionary
def json_to_dict(file):
    with open(file) as json_file:  
        data = json.load(json_file)
    return data 