from upd.model import *
from flask_wtf import Form
from wtforms import FormField, FieldList, BooleanField, TextField, PasswordField, SelectField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(Form):
  username = TextField('username', [validators.Required()])
  password = PasswordField('password')

class TestForm(Form):
  test_field = TextField("Test Field", [validators.Length(min=5, max=12)])
  pie_group = SelectField(u'The Pie Group', coerce=int)
  ingredient_category = SelectField("Ingredient Category")

class TheTestForm(Form):
  ingredients = FieldList(FormField(TestForm))

def fill_field():
  return RecipeCategory.query

class AnotherTestForm(Form):
  my_field = QuerySelectField(query_factory=fill_field, get_label='recipe_cat_name')

class YATF(Form):
  my_fields = FieldList(FormField(AnotherTestForm))


def form_recipe_query():
  return Recipe.query.order_by(Recipe.recipe_name)

def form_food_des_query():
  return FOOD_DES.query.order_by(FOOD_DES.Long_Desc)

def ingredient_label(ingredient):
  Shrt_Desc = ingredient.food_des.Shrt_Desc
  weight_value = ingredient.weight_value
  Msre_Desc = WEIGHT.query.get((ingredient.NDB_No, ingredient.Seq)).Msre_Desc
  return "%s, %s %s" % (Shrt_Desc, weight_value, Msre_Desc)

# form to map ingredients to recipes
class IngredientMapForm(Form):
  recipe_name = QuerySelectField(u'Pie Recipe', query_factory=form_recipe_query, get_label='recipe_name')
  ingredient = QuerySelectField(u'Ingredient Name', query_factory=form_food_des_query, get_label='Long_Desc')
  Seq = SelectField(u'Weight Sequence')
  weight_value = TextField(u'Weight value ', [validators.NumberRange(), validators.Required()])

class IngredientMapFormDel(Form):
  recipe_name = QuerySelectField(u'Pie Recipe', query_factory=form_recipe_query, get_label='recipe_name')
  ingredient = QuerySelectField(get_label=ingredient_label)
