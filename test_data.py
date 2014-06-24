#!/usr/bin/python

import upd
from upd.model import *

db.create_all()

nick = Author("Firsty", "Lasty", "ultimatepiday@gmail.com", "Nick", "http://www.ultimatepiday.com/")
fruit_pies = RecipeCategory("Fruit Pies", "A category concerning pies of the fruit persuasion.")
banana_pie = Recipe("Banana Pie", 1, 1, 45*60, 1, 350)
banana_pie_directions = [ "Direction one", "Direction two", "Direction three", "Direction four", "Direction Five" ]

omg_delicious_butter = Ingredient(1, "01001", 4, 8)

db.session.add(nick)
db.session.add(fruit_pies)
db.session.add(banana_pie)

for idx,val in enumerate(banana_pie_directions, start=1):
  step = Directions(1, idx, val)
  db.session.add(step)


db.session.commit()




db.session.add(omg_delicious_butter)
db.session.commit()

# TODO: Add test data for Ingredients

