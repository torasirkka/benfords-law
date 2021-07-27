from flask import Flask, request, render_template

import pandas as pd
import plotly
import plotly.graph_objs as go
import json
import numpy as np
import scipy.stats as stats

from typing import Any, Tuple

# I'm storing submitted files under the following filename.
# Each time a new file is submitted, this one is overwritten
FILENAME = "dataset"

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def upload_file():
  # check if the post request has the file part
  if 'file' not in request.files:
    return render_template('index.html')
  file = request.files['file']
  
  # check that col name is provided:
  if request.form['col_name'] == "":
    return render_template('index.html')
  col_name = request.form['col_name']

  # If the user does not select a file: redirect back to start.
  if file.filename == '':
      return render_template('index.html')
  if file:
      # save file locally
      file.save(FILENAME)

      # read in dataframe
      df = pd.read_table(FILENAME)

      # validate column name
      if col_name not in df.columns:
        return render_template('index.html')

      # generate bar plot data
      bar, p_val = _benford_plot(df, col_name)
      
      if p_val < 0.5:
        analysis = "significantly different"
      else: 
        analysis = "not significantly different"


      # send bar plot data to front end 
      return render_template('data.html', plot=bar, analysis=analysis)


def _first_num(i:int)->int:
  """Return the first digit of an int."""
  
  # convert int to str, then slice out first digit, convert 
  # it back to an int and return it.
  s = str(i)
  return int(s[0])

def _benford_plot(df: pd.DataFrame, col_name: str)-> Tuple(Any,bool):
  """Dataframe that generates a benford bar plot describing the probability
  distribution for the first digit of the numbers in col_name."""

  # slice out the dataset (pandas series) we're interested in
  nums = df[col_name].apply(_first_num)

  # filter out zeroes and Nan values
  observed = nums[(nums != 0)].value_counts(normalize=True, dropna=True)

  # add col with theoretical values for easier interpretation of results
  theoretical_vals = pd.Series(
    [0.334,0.185,0.124,0.075,0.071,0.065,0.055,0.049,0.042],
    index = [1,2,3,4,5,6,7,8,9],
    name='Benfords Law'
    )
  plot_data = pd.concat([observed, theoretical_vals], axis = 1)

  # Analyze how well the data fits with the predicted frequency distribution
  p_val = _chi_squared_GOF(theoretical_vals, observed)

  # plot resuts
  data = [go.Bar(y = plot_data[col_name], x = plot_data.index, name=f'Submitted dataset: {col_name}.'),
          go.Bar(y = plot_data["Benfords Law"], x=plot_data.index, name="Benford's Law Prediction")]

  graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
  return (graphJSON, analysis)


def _chi_squared_GOF(expected: pd.Series, observed: pd.Series):
    """
    Runs a chi-square goodness-of-fit test and returns the p-value.
    Inputs:
    - expected: numpy array of expected values.
    - observed: numpy array of observed values.
    Returns: p-value
    """
    expected_scaled = expected / float(sum(expected)) * sum(observed)
    result = stats.chisquare(f_obs=observed, f_exp=expected_scaled)
    return result[1]


if __name__ == '__main__':
  app.secret_key = 'super secret key' 
  app.run(debug=True, host="0.0.0.0")


