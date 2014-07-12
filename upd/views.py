from upd import app, login_manager
from flask.ext.login import login_required, login_user, logout_user, current_user
from upd.model import *
from flask import render_template, request, url_for, flash, redirect, jsonify
from forms import *


@login_manager.user_loader
def load_user(userid):
  return User.query.get(int(userid))

def logout():
  logout_user()
  return redirect(url_for("index"))

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  if form.validate_on_submit():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
      if user.check_password(password):
        login_user(user)
        flash("Logged in successfully")
        return redirect(request.args.get("next") or url_for("index"))
    flash("Unsuccessful login attempt.")
  return render_template("login.html", form=form)

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


@app.route("/api/ingredient_map/<action>", methods=['GET', 'POST'])
@login_required
def add_ingredient_map(action="add"):
  if action == "add":
    form = IngredientMapForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
      if form.ingredient.validate(form):
        ingredient = form.ingredient.data
        form.Seq.choices = [(i.Seq,i.Msre_Desc) for i in WEIGHT.query.filter_by(NDB_No=ingredient.NDB_No).all()]
        if form.validate_on_submit():
          message = "All things found: (%s, %s, %s, %s)" % (form.recipe_name.data, form.ingredient.data, form.Seq.data, form.weight_value.data)
          print message
          flash(message)
          return redirect(url_for('omfg'))
        else:
          print form.errors
    if not form.Seq.choices:
      form.Seq.choices = []
    return render_template('add_ingredient_map.html', form=form)
  elif action == "delete":
    form = IngredientMapFormDel(request.form, csrf_enabled=False)
    if request.method == 'POST':
      if form.recipe_name.validate(form):
        form.ingredient.choices = [(1, 'moo')]
      if form.validate_on_submit():
        print "Deleting: %s %s" % (form.ingredient.data, form.recipe_name.data)
        return "OK"
    if not form.ingredient.choices:
      form.ingredient.choices = []
    return render_template('delete_ingredient_map.html', form=form)
  else:
    return "Operation not supported"
