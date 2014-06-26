###########
#
# Documentation: lol python is self documenting
#
##########
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from upd import app

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), unique=True)
  email = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())

  def __init__(self, username, password, email):
    self.username = username
    self.set_password(password)
    self.email = email
    self.active = True

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

class Ingredient(object):
  query = db.session.query_property()

  def __init__(self, recipe_num, NDB_No, Seq, weight_value):
    self.recipe_num = recipe_num
    self.NDB_No = NDB_No
    self.Seq = Seq
    self.weight_value = weight_value

  def __repr__(self):
    return '<Ingredient %s>' % (str(self.recipe_num) + " - " + self.NDB_No)


ingredients_tbl = db.Table('ingredients_tbl',
  db.Column('recipe_num', db.INT(), db.ForeignKey('upd.Recipe.recipe_num'), primary_key=True),
  db.Column('NDB_No', db.CHAR(5), db.ForeignKey('sr26.FOOD_DES.NDB_No'), primary_key=True),
  db.Column('Seq', db.CHAR(2), db.ForeignKey('sr26.WEIGHT.Seq')),
  db.Column('weight_value', db.INT()),
  info={'bind_key': 'upd'},
  schema='upd',
)

db.mapper(Ingredient, ingredients_tbl)

# Category
class RecipeCategory(db.Model):
  __bind_key__ = 'upd'
  __tablename__ = 'RecipeCategory'
  __table_args__ = {'schema':'upd'}
  recipe_cat_num = db.Column(db.INT(), primary_key = True)
  recipe_cat_name = db.Column(db.VARCHAR(200))
  recipe_cat_desc = db.Column(db.Text())

  def __init__(self, recipe_cat_name, recipe_cat_desc):
    self.recipe_cat_name = recipe_cat_name
    self.recipe_cat_desc = recipe_cat_desc


class Recipe(db.Model):
  __bind_key__ = 'upd'
  __tablename__ = 'Recipe'
  __table_args__ = {'schema':'upd'}
  recipe_num = db.Column(db.INT(), primary_key = True)
  recipe_cat_num = db.Column(db.INT(), db.ForeignKey('upd.RecipeCategory.recipe_cat_num'))
  recipe_category = db.relationship('RecipeCategory', backref=db.backref('q_recipes', lazy='dynamic'))
  author_num = db.Column(db.INT(), db.ForeignKey('upd.Author.author_num'))
  author = db.relationship('Author', backref=db.backref('q_recipes'))
  recipe_name = db.Column(db.VARCHAR(120))
  cook_time = db.Column(db.INT())
  pie_yield = db.Column(db.INT())
  cook_temp = db.Column(db.INT())
  ingredients = db.relationship('FOOD_DES', secondary=ingredients_tbl, backref="q_recipes", lazy="dynamic")

  def __init__(self, recipe_name, recipe_cat_num, author_num, cook_time, pie_yield, cook_temp):
    self.recipe_name = recipe_name
    self.recipe_cat_num = recipe_cat_num
    self.author_num = author_num
    self.cook_time = cook_time
    self.pie_yield = pie_yield
    self.cook_temp = cook_temp

class RecipePictures(db.Model):
  __bind_key__ = 'upd'
  __tablename__ = 'RecipePictures'
  __table_args__ = {'schema':'upd'}
  recipe_num = db.Column(db.INT(), db.ForeignKey('upd.Recipe.recipe_num'), primary_key = True)
  recipe = db.relationship('Recipe', backref=db.backref('q_pictures'))
  picture_num = db.Column(db.INT(), primary_key = True, autoincrement=False)
  picture_hash = db.Column(db.VARCHAR(64))
  picture_name = db.Column(db.TEXT())

  def __init__(self, recipe_num, picture_num, picture_hash, picture_name):
    self.recipe_num = recipe_num
    self.picture_num = picture_num
    self.picture_hash = picture_hash
    self.picture_name = picture_name


# Author
class Author(db.Model):
  __bind_key__ = 'upd'
  __tablename__ = 'Author'
  __table_args__ = {'schema':'upd'}
  author_num = db.Column(db.INT(), primary_key = True)
  first_name = db.Column(db.VARCHAR(40))
  last_name = db.Column(db.VARCHAR(40))
  email_address = db.Column(db.VARCHAR(200))
  alias = db.Column(db.VARCHAR(60))
  website = db.Column(db.VARCHAR(200))

  def __init__(self, first_name, last_name, email_address, alias, website):
    self.first_name = first_name
    self.last_name = last_name
    self.email_address = email_address
    self.alias = alias
    self.website = website

# Directions
class Directions(db.Model):
  __bind_key__ = 'upd'
  __tablename__ = 'Directions'
  __table_args__ = {'schema':'upd'}
  recipe_num = db.Column(db.INT(), db.ForeignKey('upd.Recipe.recipe_num'), primary_key = True)
  step_num = db.Column(db.INT(), primary_key = True, autoincrement=False)
  step_text = db.Column(db.TEXT())
  recipe = db.relationship('Recipe', backref=db.backref('q_directions'))

  def __init__(self, recipe_num, step_num, step_text):
    self.recipe_num = recipe_num
    self.step_num = step_num
    self.step_text = step_text


# This is the data model for the sr26 database

class NUT_DATA(db.Model):
  __bind_key__ = 'sr26'
  __table_args__ = {'schema' : 'sr26'}
  NDB_No = db.Column(db.CHAR(5), db.ForeignKey('sr26.FOOD_DES.NDB_No'), primary_key = True )
  food_desc = db.relationship('FOOD_DES', backref=db.backref('q_nut_datas', lazy='dynamic'))
  Nutr_No = db.Column(db.CHAR(3), db.ForeignKey('sr26.NUTR_DEF.Nutr_No'), primary_key = True)
  nut_def = db.relationship('NUTR_DEF', backref=db.backref('q_nut_datas', lazy='dynamic'))
  Nutr_Val = db.Column(db.Float(10,3))
  Num_Data_Pts = db.Column(db.Float(5, 0))
  Std_Error = db.Column(db.Float(8, 3))
  Src_Cd = db.Column(db.CHAR(2))
  Deriv_Cd = db.Column(db.CHAR(4))
  Ref_NDB_No = db.Column(db.CHAR(5))
  Add_Nutr_Mark = db.Column(db.CHAR(1))
  Num_Studies = db.Column(db.Integer())
  Min = db.Column(db.Float(10, 3))
  Max = db.Column(db.Float(10, 3))
  DF  = db.Column(db.Integer())
  Low_EB = db.Column(db.Float(10, 3))
  Up_EB = db.Column(db.Float(10, 3))
  Stat_cmt = db.Column(db.CHAR(10))
  AddMod_Date = db.Column(db.CHAR(10))
  CC  = db.Column(db.CHAR(1))

  def __repr__(self):
    return "<NUT_DATA %s>" % (self.NDB_No + " - " + self.Nutr_No)

class FOOD_DES(db.Model):
  __bind_key__ = 'sr26'
  __tablename__ = 'FOOD_DES'
  __table_args__ = {'schema' : 'sr26'}
  NDB_No = db.Column(db.CHAR(5), primary_key = True)
  FdGrp_Cd = db.Column(db.CHAR(4), db.ForeignKey('sr26.FD_GROUP.FdGrp_Cd'))
  food_group = db.relationship('FD_GROUP', backref=db.backref('q_food_desc', lazy='dynamic'))
  Long_Desc = db.Column(db.VARCHAR(200))
  Shrt_Desc = db.Column(db.VARCHAR(60))
  ComName = db.Column(db.VARCHAR(100))
  ManufacName = db.Column(db.VARCHAR(65))
  Survey = db.Column(db.CHAR(1))
  Ref_desc = db.Column(db.VARCHAR(135))
  Refuse = db.Column(db.INT())
  SciName = db.Column(db.VARCHAR(65))
  N_Factor = db.Column(db.FLOAT(4, 2))
  Pro_Factor = db.Column(db.FLOAT(4, 2))
  Fat_Factor = db.Column(db.FLOAT(4, 2))
  CHO_Factor = db.Column(db.FLOAT(4, 2))

  def __repr__(self):
    return "<FOOD_DES %s>" % self.Long_Desc

  @property
  def serialize(self):
    """Return object data in easiliy serializable format"""
    return {
      'NDB_No': self.NDB_No,
      'FdGrp_Cd': self.FdGrp_Cd,
      'Long_Desc': self.Long_Desc,
      'Shrt_Desc': self.Shrt_Desc,
    }
    

class FD_GROUP(db.Model):
  __bind_key__ = 'sr26'
  __table_args__ = {'schema' : 'sr26'}
  FdGrp_Cd = db.Column(db.CHAR(4), primary_key = True)
  FdGrp_Desc = db.Column(db.VARCHAR(60))

  def __repr__(self):
    return "<FD_GROUP %s>" % self.FdGrp_Desc

  @property
  def serialize(self):
    """Return object data in easiliy serializable format"""
    return {
      'FdGrp_Cd': self.FdGrp_Cd,
      'FdGrp_Desc': self.FdGrp_Desc,
    }

class NUTR_DEF(db.Model):
  __bind_key__ = 'sr26'
  __table_args__ = {'schema' : 'sr26'}
  Nutr_No = db.Column(db.CHAR(3), primary_key = True)
  Units = db.Column(db.CHAR(7))
  Tagname = db.Column(db.VARCHAR(20))
  NutrDesc = db.Column(db.VARCHAR(60))
  Num_Dec = db.Column(db.INT())
  SR_Order = db.Column(db.INT())

  def __repr__(self):
    return "<NUTR_Def %s>" % self.NutrDesc

class WEIGHT(db.Model):
  __bind_key__ = 'sr26'
  __table_args__ = {'schema' : 'sr26'}
  NDB_No = db.Column(db.CHAR(5), db.ForeignKey('sr26.FOOD_DES.NDB_No'), primary_key = True)
  food_desc = db.relationship('FOOD_DES', backref=db.backref('q_weights', lazy='dynamic'))
  Seq = db.Column(db.CHAR(2), primary_key = True, index = True)
  Amount = db.Column(db.FLOAT(5, 3))
  Msre_Desc = db.Column(db.VARCHAR(84))
  Gm_Wgt = db.Column(db.FLOAT(7,1))
  Num_Data_Pts = db.Column(db.INT())
  Std_Dev = db.Column(db.FLOAT(7,3))

  def __repr__(self):
    return "<WEIGHT %s>" % (self.NDB_No + " - " + self.Seq)

  @property
  def serialize(self):
    """Return object data in easily serializable format"""
    return {
      'NDB_No': self.NDB_No,
      'Seq': self.Seq,
      'Amount': self.Amount,
      'Msre_Desc': self.Msre_Desc,
      'Gm_Wgt': self.Gm_Wgt,
    }

class FOOTNOTE(db.Model):
  __bind_key__ = 'sr26'
  __table_args__ = {'schema' : 'sr26'}
  NDB_No = db.Column(db.CHAR(5), primary_key = True)
  Footnt_No = db.Column(db.CHAR(4))
  Footnt_Typ = db.Column(db.CHAR(1))
  Nutr_No = db.Column(db.CHAR(3))
  Footnt_Txt = db.Column(db.VARCHAR(200))
