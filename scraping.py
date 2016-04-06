
import requests
import pandas as pd
import os
from sqlalchemy import create_engine

#%%

os.chdir("/tmp")

engine = create_engine('sqlite:///car2go.db')


#%%

url = "https://www.car2go.com/api/v2.1/vehicles?loc=duesseldorf&oauth_consumer_key=car2gowebsite&format=json"
# https://www.car2go.com/api/v2.1/operationareas?loc=duesseldorf&oauth_consumer_key=car2gowebsite&format=json

# call API 
r = requests.get(url)

#%%

r.status_code
hdr = r.headers

print(hdr["Date"])

#r.encoding
#r.text

#%%

# jdta = r.json()
# same: data = json.loads(r.text)

if r.status_code == requests.codes.ok:
    # car2go returns everything inside a placemarks [], so we normalise here
    data = pd.io.json.json_normalize(r.json(), 'placemarks')
    
    #data.dtypes
    # coordinates throws error when exporting to db TEXT field    
    # convert location into string to export to db later
    #data["test"] = data["coordinates"].astype(str)
    
    # split coordinates column into "normal" columns to input into db later
    data['long'] = data['coordinates'].apply(lambda x: x[0])
    data['lat'] = data['coordinates'].apply(lambda x: x[1])
    data['elevation'] = data['coordinates'].apply(lambda x: x[2])
    # drop coordinates column to avoid error when appending to db 
    data.drop('coordinates', axis=1, inplace=True)
    # add API call time to df
    data["APIcall"] = pd.to_datetime(hdr["Date"])

    # write to db
    data.to_sql('car2go', engine, if_exists='append', index=False)
else:
    err = {'errorCode': r.status_code, 'APIcall': pd.to_datetime(hdr["Date"])}
    err = pd.DataFrame(err, index=[0])
    err.to_sql('error2go', engine, if_exists='append', index=False)

#%%