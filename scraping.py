
import requests
import pandas as pd
import os
from sqlalchemy import create_engine
import datetime
from time import sleep

#%%

def create_car2go_engine(location = '/tmp', name = 'car2go.db'):

    engine = create_engine('sqlite:///'+os.path.join(location, name))
    return engine
    
engine = create_car2go_engine()
    
#%%

def call_API_dump_to_db(): 
    
    # car2go API
    url = "https://www.car2go.com/api/v2.1/vehicles?loc=duesseldorf&oauth_consumer_key=car2gowebsite&format=json"
    # https://www.car2go.com/api/v2.1/operationareas?loc=duesseldorf&oauth_consumer_key=car2gowebsite&format=json

    # call API 
    r = requests.get(url)
    
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
        data["APIcall"] = pd.to_datetime(r.headers['Date'])
        
        # write to db
        data.to_sql('car2go', engine, if_exists='append', index=False)
    else:
        err = {'errorCode': r.status_code, 'APIcall': pd.to_datetime(r.headers['Date'])}
        err = pd.DataFrame(err, index=[0])
        err.to_sql('error2go', engine, if_exists='append', index=False)

#%%


# stop_at needs to be a string in the format "%Y-%m-%d %H:%M:%S UTC"
# e.g. "2016-04-07 12:25:00 UTC"
def API_call_loop(interval = 1, stop_at = None):
    
    # mutable default arguments: http://docs.python-guide.org/en/latest/writing/gotchas/
    # default to 15 seconds from utcnow()    
    if stop_at is None:
        stop_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=15)
    else:
        stop_at = datetime.datetime.strptime(stop_at, "%Y-%m-%d %H:%M:%S UTC")

    while (datetime.datetime.utcnow() < stop_at):
        print("I'm at:", format(datetime.datetime.utcnow()), "UTC")
        #call_API_dump_to_db()
        sleep(interval)

#%%








