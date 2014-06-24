from upd.model import *
from flask_wtf import Form
from wtforms import FormField, FieldList, BooleanField, TextField, PasswordField, SelectField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class TestForm(Form):
  test_field = TextField("Test Field", [validators.Length(min=5, max=12)])
  pie_group = SelectField(u'The Pie Group', coerce=int)
  ingredient_category = SelectField("Ingredient Category")

class TheTestForm(Form):
  ingredients = FieldList(FormField(TestForm))

def fill_field():
  return RecipeCategory.query

print 'form imported'
# this seems to be a dynamic way. I don't understand how queryselectfield is re-running the select every instantiation..but this seems to be the case(??)
class AnotherTestForm(Form):
  my_field = QuerySelectField(query_factory=fill_field, get_label='recipe_cat_name')
  print 'atf instantiated'

class YATF(Form):
  my_fields = FieldList(FormField(AnotherTestForm))




# http://stackoverflow.com/questions/19898967/how-to-use-wtforms-in-ajax-validation
