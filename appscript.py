import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# dictionary to define query parameters

options_dict = {
    'Severe Storms': 'severeStorms',
    'Volcanoes': 'volcanoes',
    'Sea/Lake Ice': 'seaLakeIce',
    'Wildfires': 'wildfires'
}

# color mapping for each category to display on map
color_map = {
    'Wildfires': 'red',
    'Volcanoes': 'brown',
    'Sea/Lake Ice': 'blue',
    'Severe Storms': 'orange'
}


# title and description at the top
st.title("Open Events Location Map")
st.markdown("""
This map displays the geographic locations of events. On the right tab you can select phenomenon that you are interested in. 
You can hover over each point to see additional information, such as the event start date and category.
Queried data is based on available data from NASA EONET API v3.
""")

# keys of dict for display
display_options = list(options_dict.keys())



# sidebar with multiple selection box
st.sidebar.title("Query Options")
selected_display_options = st.sidebar.multiselect('Select open event (disaster):', display_options)


# always display an empty map
fig = px.scatter_geo(lat=[], lon=[], projection="natural earth",width=1000, height=800)


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
    else:
        st.error(f"Error: Unable to fetch data (Status code: {response.status_code})")
        return None

# separate functions for each event category, while fetching all for some reason coordinates get messed up on the map
def fetch_wildfires(limit=10):
    return get_live_events(status='open', categories=['wildfires'], limit=limit)

def fetch_volcanoes(limit=10):
    return get_live_events(status='open', categories=['volcanoes'], limit=limit)

def fetch_severe_storms(limit=10):
    return get_live_events(status='open', categories=['severeStorms'], limit=limit)

def fetch_sea_lake_ice(limit=10):
    return get_live_events(status='open', categories=['seaLakeIce'], limit=limit)

# initialize an empty df to hold the event data
geo_coord = pd.DataFrame()

# fetch data using defined function and concatenate populate empty df
if 'Wildfires' in selected_display_options:
    #st.subheader('Wildfires')
    wildfires_data = fetch_wildfires(limit=10000)
    if wildfires_data is not None:
        geo_coord = pd.concat([geo_coord, wildfires_data])

if 'Volcanoes' in selected_display_options:
    #st.subheader('Volcanoes')
    volcanoes_data = fetch_volcanoes(limit=10000)
    if volcanoes_data is not None:
        geo_coord = pd.concat([geo_coord, volcanoes_data])

if 'Severe Storms' in selected_display_options:
    #st.subheader('Severe Storms')
    storms_data = fetch_severe_storms(limit=10000)
    if storms_data is not None:
        geo_coord = pd.concat([geo_coord, storms_data])

if 'Sea/Lake Ice' in selected_display_options:
    #st.subheader('Sea/Lake Ice')
    sea_lake_ice_data = fetch_sea_lake_ice(limit=10000)
    if sea_lake_ice_data is not None:
        geo_coord = pd.concat([geo_coord, sea_lake_ice_data])




if not geo_coord.empty:
    fig = px.scatter_geo(geo_coord,
                         lat='latitude',
                         lon='longitude',
                         hover_name='title',
                         hover_data={
                             'date': True
                         },
                         projection="natural earth",   # map projection type
                         color='category',             # color based on category
                         color_discrete_map=color_map,
                         width=1000, height=800
                         )  

# update the layout to add water and land colors and hide the legend
fig.update_geos(
    showocean=True,
    oceancolor="lightblue",
    showland=True,
    landcolor="lightgreen",
    showlakes=True,
    lakecolor="lightblue",
    showrivers=True,
    rivercolor="lightblue"
)

# hide the legend and reduce the space between main description and text and map
fig.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=0, b=0),
    height=300
)


# show the plot
st.plotly_chart(fig)

# title and description at the top
st.title("Table view")
st.markdown("""
This table allows you to download your results in .csv file and to see more details regarding your recent query.
""")


st.dataframe(geo_coord)