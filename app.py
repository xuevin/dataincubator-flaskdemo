from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import numpy as np
import pandas as pd
import matplotlib

from bokeh.embed import components
from bokeh.charts import Line

app = Flask(__name__)


def getPlot(ticker):
   ticker='GOOG'
   r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'/data.json?api_key=Eebg1xGXqxhS11D52xGs')
   asJson = json.loads(r.content)
   dataFormated = pd.DataFrame(np.array(asJson['dataset_data']['data']),columns=asJson['dataset_data']['column_names'])
   dataFormated['Date']=pd.to_datetime(dataFormated.Date)
   dataFormated['Open'] = pd.to_numeric(dataFormated.Open)

   #dates = matplotlib.dates.date2num(asDateTime.tolist())
   #values = np.array(dataFormated.Open).astype(float)
   line = Line(dataFormated,x='Date',y='Open',title="Cool")

   #line = Line(x=dates,y=values,title="Cool")

   return line

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

app.vars = {}
@app.route('/stock')
def stock():
   return render_template('stock.html')

@app.route('/stockVisualize',methods=['GET','POST'])
def stockVisualize():
   if request.method == 'GET':
	return "oops"
   else:
      app.vars['stockTicker'] = request.form['ticker']
      thisLine = getPlot(app.vars['stockTicker'])
      script, div = components(thisLine)
      return render_template('stockVisualize.html',stockTicker=app.vars['stockTicker'],
      script=script,div=div)

if __name__ == '__main__':
  app.run(port=33507)
