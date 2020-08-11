import json
import requests
import pandas as pd
import os
from datetime import datetime

with open('keys.json', 'r') as f:
    keys = json.load(f)

api_key = keys['api_key']
mpan = keys['mpan']
meter_id = keys['meter_id']

url = "https://api.octopus.energy/v1/electricity-meter-points/{}/meters/{}/consumption/".format(mpan, meter_id)

def get_consumption(url, api_key, save_csv = False):    
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
    
    df['start_date'] = df.interval_start.apply(lambda x: x.date().strftime('%Y-%m-%d'))
    df['end_date'] = df.interval_end.apply(lambda x: x.date().strftime('%Y-%m-%d'))
    df['start_hour'] = df.interval_start.apply(lambda x: x.hour)
    df['start_minute'] = df.interval_start.apply(lambda x: x.minute)
    df['end_hour'] = df.interval_end.apply(lambda x: x.hour)
    df['end_minute'] = df.interval_end.apply(lambda x: x.minute)
    # if save_csv:
    #     os.chdir('./data/imports')
    #     folder_name = datetime.today().strftime('%Y%m%d')
    #     file_n = 1
    #     file_name = '{}.csv'.format(file_n)
    #     if not os.path.exists(folder_name):
    #         os.mkdir(folder_name)
            
    #     while os.path.isfile('{}/{}'.format(folder_name, file_name)):
    #         file_n += 1
    #         file_name = '{}.csv'.format(file_n)

    #     os.chdir(folder_name)
    #     df.to_csv(file_name)
    return df

def get_tariffs():
    pass

def main():
    cons = get_consumption(url, api_key)
    cons.to_csv('./outputs/energy_data.csv')

if __name__ == '__main__':
    main()