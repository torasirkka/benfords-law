from flask import Flask, request, render_template
import pandas as pd
app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/data', methods = ['POST'])
def data():

  # get the submitted form
  f = request.form['flatfile']
  col_name = "7_2009"
  df = pd.read_table(f)
  nums = df[col_name].apply(first_num)

  # plot resuts
  ax = df.plot.hist(bins=9, alpha = 0.5)
  #save img locally
  ax.figure.savefig('histogram.png')
  
  return render_template('data.html')

def first_num(i:int)->int:
  """Return the first digit of an int."""
  
  # convert int to str, then slice out first digit, convert 
  # it back to an int and return it.
  s = str(i)
  return int(s[0])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
