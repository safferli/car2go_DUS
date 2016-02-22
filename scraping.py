import json
import urllib2

url = "https://www.car2go.com/api/v2.1/vehicles?loc=duesseldorf&oauth_consumer_key=car2gowebsite&format=json"

data = json.load(urllib2.urlopen(url))
