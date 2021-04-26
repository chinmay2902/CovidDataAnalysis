import pandas as pd
import folium

PData=pd.read_csv("PData.csv")


def ConfiredCasesMap():
    covid_data_max = PData['Confirmed'].max()
    world_geo = "world_countries.json"
    world_map = folium.Map(location=[4.68, 8.33], zoom_start=3)
    scale=[0,int((covid_data_max)/40),int((covid_data_max)/5),int((covid_data_max)/2.5),covid_data_max]

    world_map = folium.Choropleth(
        geo_data=world_geo,
    #     name='choropleth',
        data=PData,
        columns=['Country','Confirmed'],
        key_on='feature.properties.name',
        threshold_scale = scale,
        fill_color='Spectral',#Blues-for recovery
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of Confirmed cases per country',
        highlight=True,
        line_color='black',
    ).add_to(world_map)
    folium.LayerControl().add_to(world_map)
    world_map.save('templates/mapCases.html')

def RecoveredCasesMap():
    covid_data_max = PData['Recovered'].max()
    world_geo = "world_countries.json"
    world_map = folium.Map(location=[4.68, 8.33], zoom_start=3)
    scale=[0,int((covid_data_max)/64),int((covid_data_max)/8),int((covid_data_max)/4),int((covid_data_max)/3),int((covid_data_max)/2),covid_data_max]
    world_map = folium.Choropleth(
        geo_data=world_geo,
        name='choropleth',
        data=PData,
        columns=['Country','Recovered'],
        key_on='feature.properties.name',
        threshold_scale = scale,
        fill_color='Greens',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of People Recovered per Country',
        highlight=True,
        line_color='black'
    ).add_to(world_map)
    folium.LayerControl().add_to(world_map)
    world_map.save('templates/mapRecovered.html')

def DeathsCasesMap():
    covid_data_max = PData['Deaths'].max()
    world_geo = "world_countries.json"
    world_map = folium.Map(location=[4.68, 8.33], zoom_start=3)
    scale=[0,int((covid_data_max)/32), int((covid_data_max)/16),int((covid_data_max)/8),int((covid_data_max)/4),int((covid_data_max)/2),covid_data_max]
    world_map = folium.Choropleth(
        geo_data=world_geo,
        name='choropleth',
        data=PData,
        columns=['Country','Deaths'],
        key_on='feature.properties.name',
        threshold_scale = scale,
        fill_color='Reds',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of Deaths per Country',
        highlight=True,
        line_color='black'
    ).add_to(world_map)
    folium.LayerControl().add_to(world_map)
    world_map.save('templates/mapDeaths.html')