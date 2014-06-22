from flask_wtf import Form
from wtforms import BooleanField, TextField, PasswordField, SelectField, validators

class TestForm(Form):
  test_field = TextField("Test Field", [validators.Length(min=5, max=12)])
  pie_group = SelectField(u'The Pie Group', coerce=int)
  ingredient_category = SelectField("Ingredient Category")
