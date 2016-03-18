
import requests
import pandas as pd

#%%

url = "https://www.car2go.com/api/v2.1/vehicles?loc=duesseldorf&oauth_consumer_key=car2gowebsite&format=json"

r = requests.get(url)

#%%

r.status_code
r.headers
#r.encoding
#r.text

r.status_code == requests.codes.ok

#%%

# jdta = r.json()
# same: data = json.loads(r.text)

#%%

# car2go returns everything inside a placemarks [], so we normalise here
data = pd.io.json.json_normalize(r.json(), 'placemarks')

#%%