from flask import Flask,render_template
import pandas as pd
import folium
PData=pd.read_csv("PData.csv")
app = Flask(__name__)

@app.route('/')
def map():
    
    return render_template("index.html")

@app.route('/india')
def india_map():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)