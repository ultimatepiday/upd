from upd import app
from upd.model import *
from flask import render_template

@app.route('/')
def index():
  return 'Heya World!'

@app.route('/all_the_foods')
def omg():
    return " \n".join([x.Long_Desc for x in FOOD_DES.query.all()])

@app.route('/omfg')
def omfg():
  return render_template('index.html', title='omfg')
