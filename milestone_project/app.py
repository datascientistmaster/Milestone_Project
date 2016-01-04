# Imports
from flask import Flask, render_template, request, redirect, url_for
from pandas import DataFrame, to_datetime
import pandas
import numpy as np
import json
import requests
import time
from datetime import datetime,timedelta
from bokeh.plotting import figure, output_file, show
from bokeh import embed
import cgi
import os

app = Flask(__name__)

selector = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  return render_template('index.html')

def plot():
	feature = request.form.getlist('feature')

	ticker = request.form['ticker']

	td = datetime.td()
	end_date = now.strftime('%Y-%m-%d')
	start_date = (now - timedelta(days=30)).strftime('%Y-%m-%d')

	URL = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?start_date='+start_date+'&end_date='+end_date+'&order=asc&api_key=eFoXAcyvLhyuB3Rsvg6o'
	r = requests.get(URL)

	request_df = DataFrame(r.json())
	df = DataFrame(request_df.ix['data','dataset'], columns = request_df.ix['column_names','dataset'])
	df.columns = [x.lower() for x in df.columns]
	df = df.set_index(['date'])
	df.index = to_datetime(df.index)

	p = figure(x_axis_type = "datetime",   title='Data from Quandle WIKI set',
              x_axis_label='Date',
              y_axis_label='Pricing')

	if 'close' in features:
	    p.line(df.index, df['close'], color='green', legend='closing price')
	return p


@app.route('/chart_page',methods=['GET','POST'])
def chart():
	plot = make_plot()
	script, div = embed.components(plot)
	return render_template('bokeh.html', script=script, div=div)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=33507)

	#app.run(debug=True)
