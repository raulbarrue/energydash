import json
import requests
import pandas as pd

with open('keys.json', 'r') as f:
    keys = json.load(f)

api_key = keys['api_key']
mpan = keys['mpan']
meter_id = keys['meter_id']

url = "https://api.octopus.energy/v1/electricity-meter-points/{}/meters/{}/consumption/".format(mpan, meter_id)

def get_consumption(url, api_key):    
    n = 1
    next_pages = True
    df = pd.DataFrame(columns=['consumption', 'interval_end', 'interval_start'])
    
    while next_pages:
        url_page = url + '?page={}'.format(n)
        response = requests.get(url_page, auth=(api_key, None))
        if response.status_code == 200:
            n += 1
            json_data = json.loads(response.text)
            df_n = pd.DataFrame(json_data['results'])
            df_n.interval_start = pd.to_datetime(df_n.interval_start)
            df_n.interval_end = pd.to_datetime(df_n.interval_end)
            df = df.append(df_n, ignore_index = True)
        else:
            next_pages = False
    return df

def get_tariffs():
    pass

def main():
    cons = get_consumption(url, api_key)
    print(cons)

if __name__ == '__main__':
    main()