import json
import pandas as pd 
import numpy as np
import plotly.express as px

india_states=json.load(open("states_india.geojson",'r'))

state_id_map={}

for feature in india_states['features']:
    feature['id']= feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm']]=feature['id']

# Cleaning the data by comparing it with GeoJson and renaming the states and UTs

India_data=India_data.drop([0])
India_data=India_data.replace("Delhi","NCT of Delhi") 
India_data= India_data.replace("Jammu and Kashmir","Jammu & Kashmir")
India_data= India_data.replace("Arunachal Pradesh","Arunanchal Pradesh")
India_data= India_data.drop([31])
India_data= India_data.replace("Andaman and Nicobar Islands","Andaman & Nicobar Island")
India_data= India_data.replace("Dadra and Nagar Haveli and Daman and Diu","Daman & Diu")
India_data= India_data.drop([37])

# Putting the state id column in our India covid dataset
India_data['id']=India_data['State'].apply(lambda x:state_id_map[x])

# Plotting the Graph
India_data['Confirmed_Density_Scale']=np.log10(India_data['Confirmed'])

fig= px.choropleth(India_data,
                   locations='id',
                   geojson=india_states,
                   color='Confirmed_Density_Scale',
                   hover_name='State',
                   hover_data=['Confirmed'],
                   title='COVID-19 Confirmed Cases Across India')
fig.update_geos(fitbounds="locations", visible=False)