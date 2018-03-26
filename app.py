from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import numpy as np
import pandas as pd
import matplotlib



app = Flask(__name__)


def getPlot(ticker):
   ticker='GOOG'
   r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'/data.json?api_key=Eebg1xGXqxhS11D52xGs')
   asJson = json.loads(r.content)
   dataFormated = pd.DataFrame(np.array(asJson['dataset_data']['data']),columns=asJson['dataset_data']['column_names'])
   asDateTime = pd.to_datetime(dataFormated.Date)

   dates = matplotlib.dates.date2num(asDateTime.tolist())
   values = np.array(dataFormated.Open).astype(float)

   line = Line([dates,values],title="Cool")

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
      #script, div = components(thisLine)
      return render_template('stockVisualize.html',stockTicker=app.vars['stockTicker'])

if __name__ == '__main__':
  app.run(port=33507)
