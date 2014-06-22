from upd import app
from upd.model import *
from flask import render_template, request, url_for, flash, redirect
from forms import *

@app.route('/')
def index():
  return 'Heya World!'

@app.route('/all_the_foods')
def omg():
    return " \n".join([x.Long_Desc for x in FOOD_DES.query.all()])

@app.route('/omfg')
def omfg():
  return render_template('index.html', title='omfg')

@app.route('/test_field', methods=['GET', 'POST'])
def test_field():
  form = TestForm(request.form)
  form.pie_group.choices = [(i.recipe_cat_num, i.recipe_cat_name) for i in RecipeCategory.query.order_by('recipe_cat_name')]
  form.ingredient_category.choices = [(i.FdGrp_Cd, i.FdGrp_Desc) for i in FD_GROUP.query.order_by('FdGrp_Desc')]
  if form.validate_on_submit():
    test_field = form.test_field.data
    pie_group = RecipeCategory.query.get(form.pie_group.data).recipe_cat_name
    flash('first flash message (test_field): ' + test_field)
    flash ('second flash message (pie_group): ' + pie_group)
    return redirect(url_for('omfg'))
  return render_template('testfield.html', form=form)
