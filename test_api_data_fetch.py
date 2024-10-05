import requests
import pandas as pd

# function to fetch live events from NASA EONET API
def get_live_events(status='open', categories=None, limit=10):
    base_url = 'https://eonet.gsfc.nasa.gov/api/v3/events'
    params = {
        'status': status,
        'limit': limit
    }
    if categories:
        params['category'] = ','.join(categories)

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        events_data = response.json().get('events', [])
        df = pd.json_normalize(events_data)
        
        # transform queried data
        df_geometry = df.explode('geometry')
        df_geometry = pd.json_normalize(df_geometry['geometry'])
        
        df_cat = pd.json_normalize(df['categories'].explode())
        df_cat_cleaned = df_cat.rename(columns={"title": "category"})[['category']]
        
        df_final = pd.concat([df.drop(columns=['geometry', 'categories']), df_geometry, df_cat_cleaned], axis=1)
        df_final_cleaned = df_final.dropna(subset=['id'])
        
        df_info = df_final_cleaned[['id', 'title', 'category', 'coordinates', 'date', 'magnitudeValue', 'magnitudeUnit']]
        df_info_cleaned = df_info.dropna(subset=['coordinates'])
        
        # split coordinates into latitude and longitude
        df_info_cleaned[['longitude', 'latitude']] = pd.DataFrame(df_info_cleaned['coordinates'].tolist(), index=df_info_cleaned.index)

        return df_info_cleaned

# Fetch the events
df = get_live_events()

print(df)
