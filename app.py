from flask import Flask,render_template
import pandas as pd
import numpy as np
import folium
import plotly.graph_objects as go
import plotly.io as pio
import json
import plotly
import matplotlib.pyplot as plt
import base64
import io
from figure import get_pie,get_pieI
import map as mp
import plotly.express as px

India=pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")

PData=pd.read_csv("PData.csv")

data=pd.read_csv("data.csv")



India_data=pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")

# Getting Geojson ready
import json
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


# dataI=pd.read_csv("dataI.csv")

data=pd.DataFrame(data)
header=["S","ObservationDate","State","Country","LU","Confirmed","Deaths","Recovered"]
data.columns=header
data=data.drop(["S","LU"],axis="columns")
data["ObservationDate"]=pd.to_datetime(data["ObservationDate"])




app = Flask(__name__)

@app.route('/')
def index():
    totalCases=str(PData.Confirmed.sum().item())
    totalDeaths=str(PData.Deaths.sum().item())
    totalRecovered=str(PData.Recovered.sum().item())
    RecoveredPer=str('%.2f'%((PData.Confirmed.sum().item()-PData.Recovered.sum().item())*100/PData.Confirmed.sum().item()))

    df4=data.groupby('ObservationDate').first().reset_index()
    df4=pd.DataFrame(df4)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df4.ObservationDate,y=df4.Confirmed,mode='lines',name='Confired',line=dict(color="Blue")))
    fig.add_trace(go.Scatter(x=df4.ObservationDate,y=df4.Deaths,mode='lines',name='Deaths',line=dict(color="Red")))
    fig.add_trace(go.Scatter(x=df4.ObservationDate,y=df4.Recovered,mode='lines',name='Recovered',line=dict(color="Green")))
    graphJSON= json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    # fig.show()
    
    # df1=data.Country
    df1=data.groupby('Country')['Confirmed'].sum()
    df1=pd.DataFrame(df1)
    df1=df1.reset_index()
    top_df1=df1.sort_values("Confirmed").tail(5)
    pieChart=get_pie(top_df1['Confirmed'],top_df1['Country'])

    mp.ConfiredCasesMap()
    mp.DeathsCasesMap()
    mp.RecoveredCasesMap()

    fig=px.bar(PData.sort_values("Confirmed").tail(12),x="Confirmed",y="Country",text="Confirmed",orientation="h",color_discrete_sequence=["black"])
    barJSON= json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("index.html",totalCases=totalCases,
    totalDeaths=totalDeaths,totalRecovered=totalRecovered,RecoveredPer=RecoveredPer,graphJSON=graphJSON,pieChart=pieChart,barJSON=barJSON)

@app.route('/india')
def country():
    deltaCases=str('%.2f'%((India.Delta_Confirmed[0])*100/India.Confirmed[0]))
    deltaRecovered=str('%.2f'%((India.Delta_Recovered[0])*100/India.Recovered[0]))
    deltaDeaths=str('%.2f'%((India.Delta_Deaths[0])*100/India.Deaths[0]))

    totalActive=str(India.Active[0])
    totalCases=str(India.Confirmed[0])
    totalDeaths=str(India.Deaths[0])
    totalRecovered=str(India.Recovered[0])
    RecoveredPer=str('%.2f'%((India.Confirmed[0]-India.Recovered[0])*100/India.Confirmed[0]))

    # df6=dataI
    # df6=df6.drop(["State","Country"],axis=1)
    # df6=df6.groupby('ObservationDate').first().reset_index()
    # df6=pd.DataFrame(df6)

    # fig=go.Figure()
    # fig.add_trace(go.Scatter(x=df6.ObservationDate,y=df6.Confirmed,mode='lines',name='Confired',line=dict(color="Blue")))
    # fig.add_trace(go.Scatter(x=df6.ObservationDate,y=df6.Deaths,mode='lines',name='Deaths',line=dict(color="Red")))
    # fig.add_trace(go.Scatter(x=df6.ObservationDate,y=df6.Recovered,mode='lines',name='Recovered',line=dict(color="Green")))
    df8=India.drop(0)
    fig=px.bar(df8.sort_values("Confirmed").tail(8),x="Confirmed",y="State",text="Confirmed",orientation="h",color_discrete_sequence=["yellow"])
    graphJSON= json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    # fig.show()
    
    # df7=dataI.groupby('State')['Confirmed'].sum()
    # df7=pd.DataFrame(df7)
    # df7=df7.reset_index()
    top_df2=df8.sort_values("Confirmed").tail(5)
    pieChart=get_pieI(top_df2['Confirmed'],top_df2['State'])

    # Plotting the Graph

    India_data['Confirmed_Density_Scale']=np.log10(India_data['Confirmed'])
    figCases= px.choropleth(India_data,
                    locations='id',
                    geojson=india_states,
                    color='Confirmed_Density_Scale',
                    hover_name='State',
                    hover_data=['Confirmed'],
                    title='COVID-19 Confirmed Cases Across India',)
    figCases.update_geos(fitbounds="locations", visible=False)
    mapJSON= json.dumps(figCases,cls=plotly.utils.PlotlyJSONEncoder)

    India_data['Recovered_Density_Scale']=np.log10(India_data['Recovered'])
    figRecovered= px.choropleth(India_data,
                    locations='id',
                    geojson=india_states,
                    color='Recovered_Density_Scale',
                    hover_name='State',
                    hover_data=['Recovered'],
                    title='COVID-19 Recovered Cases Across India',
                    color_continuous_scale=px.colors.diverging.BrBG)
    figRecovered.update_geos(fitbounds="locations", visible=False)
    mapRJSON= json.dumps(figRecovered,cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("india.html",totalCases=totalCases,deltaRecovered=deltaRecovered,deltaCases=deltaCases,deltaDeaths=deltaDeaths,totalActive=totalActive,
    totalDeaths=totalDeaths,totalRecovered=totalRecovered,RecoveredPer=RecoveredPer,graphJSON=graphJSON,pieChart=pieChart,mapJSON=mapJSON,mapRJSON=mapRJSON)

@app.route('/mapCases')
def mapCases():
    return render_template("mapCases.html")

@app.route('/mapRecovered')
def mapRecovered():
    return render_template("mapRecovered.html")

@app.route('/mapDeaths')
def mapDeaths():
    return render_template("mapDeaths.html")

# @app.route('/mapCases')
# def map():
#     return render_template("mapCases.html")

if __name__ == '__main__':
    app.run(debug=True)