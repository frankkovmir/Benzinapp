import yaml
import requests

with open('config.yaml') as file:
    cfg = yaml.full_load(file)

# Abfragen der Tankerkoenig API.
# https://creativecommons.tankerkoenig.de/

apikey = cfg['api_key']
home = "https://creativecommons.tankerkoenig.de/json/"
func = "list.php?"
lat = cfg['latitude']
lon = cfg['longitude']
rad = cfg['radius']

loca = f"lat={lat}&lng={lon}&rad={rad}"
opti = "&sort=price&type=diesel&apikey="

url = home + func + loca + opti + apikey
data = requests.get(url).json()

    
ids=""
for ts in data['stations']:
    ids += ts['id'] + ','
    
if ids[-1] == ',':
    ids = ids[:-1]

func = "prices.php?"
url = home + func + "ids=" + ids + "&apikey="+ apikey
details = requests.get(url).json()

for ts in data['stations']:
    print(f"{ts['place']}, {ts['street']} {ts['houseNumber']}: {ts['name']}")
    if ts['id'] in details['prices']:
        if details['prices'][ts['id']]['status'] == "open":
            print("  Tankstelle geöffnet")
        else:
            print("  Tankstelle geschlossen")
        print("  Diesel-Preis: ", details['prices'][ts['id']]['diesel'])