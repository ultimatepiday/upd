from upd import app
from upd.model import *
from flask import render_template, request, url_for, flash, redirect, jsonify
from forms import *

@app.route('/')
def index():
  return 'Welcome to http://www.ultimatepiday.com/'

@app.route('/omfg')
@app.route('/omfg/<testid>/')
def omfg(testid="omfg"):
  return render_template('index.html', title=testid)


# example sets up dynamic selectfield thingy
@app.route('/test_field', methods=['GET', 'POST'])
def test_field():

  ##form = TestForm()
  ##form.pie_group.choices = [(i.recipe_cat_num, i.recipe_cat_name) for i in RecipeCategory.query.order_by('recipe_cat_name')]
  ##form.ingredient_category.choices = [(i.FdGrp_Cd, i.FdGrp_Desc) for i in FD_GROUP.query.order_by('FdGrp_Desc')]

  #form = TheTestForm()
  #form.ingredients.append_entry()
  #form.ingredients[0].pie_group.choices = [(i.recipe_cat_num, i.recipe_cat_name) for i in RecipeCategory.query.order_by('recipe_cat_name')]
  #form.ingredients[0].ingredient_category.choices = [(i.FdGrp_Cd, i.FdGrp_Desc) for i in FD_GROUP.query.order_by('FdGrp_Desc')]

  form = YATF()
  form.my_fields.append_entry()
  
  if form.validate_on_submit():
    for key in request.form.keys():
      for value in request.form.getlist(key):
        print key, " : ", value
    #test_field = form.test_field.data
    #pie_group = RecipeCategory.query.get(form.pie_group.data).recipe_cat_name
    #flash('first flash message (test_field): ' + test_field)
    #flash ('second flash message (pie_group): ' + pie_group)
    return redirect(url_for('omfg'))
  return render_template('testfield.html', form=form)


@app.route("/api/food_groups", methods=['GET'])
def api_food_groups():
  return jsonify(results=[i.serialize for i in FD_GROUP.query.all()])

@app.route("/api/ingredients/", methods=['GET'])
@app.route("/api/ingredients/<food_group>/", methods=['GET'])
def api_ingredients(food_group=None):
  if food_group:
    return jsonify(results=[i.serialize for i in FOOD_DES.query.filter_by(FdGrp_Cd=food_group).all()])
  else:
    return jsonify(results=[i.serialize for i in FOOD_DES.query.all()])

@app.route("/api/weights/<NDB_No>", methods=['GET'])
def api_weights(NDB_No=None):
  return jsonify(results=[i.serialize for i in WEIGHT.query.filter_by(NDB_No=NDB_No).all()])


@app.route("/api/add_ingredient_map", methods=['GET', 'POST'])
def add_ingredient_map():
  form = IngredientMapForm(request.form, csrf_enabled=False)
  if request.method == 'POST':
    if form.NDB_No.validate(form):
      NDB_No = form.NDB_No.data
      form.Seq.choices = [(i.Seq,i.Msre_Desc) for i in WEIGHT.query.filter_by(NDB_No=NDB_No.NDB_No).all()]
      if form.validate_on_submit():
        print "All things found: (%s, %s, %s, %s)" % (form.recipe_num.data, form.NDB_No.data, form.Seq.data, form.weight_value.data)
        return redirect(url_for('omfg'))
      else:
        print form.errors
  if not form.Seq.choices:
    form.Seq.choices = []
  return render_template('add_ingredient_map.html', form=form)
