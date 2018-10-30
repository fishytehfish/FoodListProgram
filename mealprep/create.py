from flask import (Blueprint, flash, redirect, render_template,
                   request, url_for, session)
from mealprep.db import get_db
import numpy as np
import mealprep.selection as Selection
import mealprep.CreateGroceryList as CreateGroceryList
import mealprep.ParseRecipe as ParseRecipe
import datetime

bp = Blueprint('create', __name__)


@bp.route('/')
def index():
    return render_template('foodlist/index.html')

@bp.route('/create', methods=('GET', 'POST'))
def create_list():
    if request.method == 'POST':
        start_day = request.form['start_day'].capitalize()
        number_days = request.form['number_days']
        error = check_create_input_for_errors(start_day, number_days)
        try:
            number_days = int(number_days)
        except ValueError:
            error = 'Number of days must be a number.'
            
        if error is not None:
            flash(error)
        else:
            # create list of days to pick recipes for
            days_for_meal_prep = Selection.days_to_plan_for( 
                    start_day, number_days)
            session['days_for_meal_prep'] = days_for_meal_prep
            return redirect(url_for('create.select_recipes'))

    return render_template('foodlist/create.html')

@bp.route('/add', methods=('GET', 'POST'))
def add_recipe():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name'].capitalize()
        meal_served = request.form['meal_served'].capitalize()
        serving_size = request.form['serving_size']
        ingredient_info = request.form['ingredient_info']
        #ingredient_info is string in same format that is entered into text area
        #split ingredient info into amount, measurement, name for each ingredient
        recipe_info = ParseRecipe.parse_ingredient_info(ingredient_info)
        db = get_db()
        db.execute(
                'INSERT INTO recipe'
                ' (recipe_name, meal_served, serving_size)'
                ' VALUES (?, ?, ?)',
                (recipe_name, meal_served, serving_size))
        for ingredient in recipe_info.ingredients:
            ingredient_index = recipe_info.ingredients.index(ingredient)
            measurement = recipe_info.measurements[ingredient_index]
            amount = recipe_info.amounts[ingredient_index]
            db.execute(
                    'INSERT INTO ingredient'
                    ' (recipe_id, ingredient, measurement, amount)'
                    ' VALUES ((SELECT id from recipe WHERE recipe_name=?), ?, ?, ?)',
                    (recipe_name, ingredient, measurement, amount))
        db.commit()
        return redirect(url_for('create.index'))
    return render_template('foodlist/add.html')

@bp.route('/edit', methods=('GET', 'POST'))
def select_recipe_to_edit():
    db = get_db()
    recipes = db.execute(
            'SELECT id, recipe_name FROM recipe').fetchall()
    if request.method == 'POST':
        recipe_to_edit = request.form['edit_recipe']
        recipe_name = request.form['recipe_name']
        # get recipe_id to use to edit recipe
        session['recipe_to_edit'] = recipe_to_edit
        print(recipe_name)
        return redirect(
                url_for('create.edit_recipe', id=recipe_to_edit, recipes = recipes))
    return render_template('foodlist/recipes.html', recipes=recipes)

@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_recipe(id):
    db = get_db()
    ingredient_info = db.execute(
            'SELECT r.id, ingredient, measurement, amount'
            ' FROM recipe r'
            ' JOIN ingredient i ON r.id = i.recipe_id'
            ' WHERE r.id = ?',
            (id,)).fetchall()
#    for ingredient in ingredient_info:
#                
    # loop over ingredient_info and create lists for amounts, ingredients,
    # etc before inputting into edit.html?
    return render_template('foodlist/edit.html', ingredient_info=ingredient_info)

@bp.route('/select', methods=('GET', 'POST'))
def select_recipes():
    days_for_meal_prep = session.get('days_for_meal_prep')
    meals = ['Breakfast', 'Lunch', 'Dinner']
    session['meals'] = meals
    db = get_db()
    recipes = db.execute(
            'SELECT recipe_name, meal_served, serving_size'
            ' FROM recipe').fetchall()
    if request.method == 'POST':
        picked_recipes = request.form.getlist('select_recipes')
        session['picked_recipes'] = picked_recipes
        error = None
        
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('create.grocery_list'))
    return render_template('/foodlist/selection.html', meals=meals,
                           days=days_for_meal_prep, recipes=recipes)
    
@bp.route('/grocerylist', methods=('GET', 'POST'))
def grocery_list():
    db = get_db()
    recipes = db.execute(
            'SELECT recipe_name, meal_served, serving_size'
            ' FROM recipe').fetchall()
    days_for_meal_prep = session.get('days_for_meal_prep')
    picked_recipes = session.get('picked_recipes')
    meals = session.get('meals')
    grocery_df = CreateGroceryList.create_grocery_list(
            recipes, picked_recipes)
    ingredient_names = grocery_df['Name'].tolist()
    ingredient_amounts = grocery_df['Amount'].tolist()
    ingredient_measurements = grocery_df['Measurement'].tolist()
    # zip together lists and iterate over them to combine elements at same index
    # from each list as string into combined list
    grocery_list = combine_ingredient_lists(ingredient_names,
                                            ingredient_amounts,
                                            ingredient_measurements)
    if request.method == 'POST':
        if request.form['store_button'] == 'Save As':
            save_as(grocery_df, picked_recipes)
        elif request.form['store_button'] == 'Email':
            # NOT IMPLEMENTED
#            email()
            flash("Not implemented")
    return render_template('/foodlist/grocerylist.html',
                           grocery_list=grocery_list,
                           days=days_for_meal_prep,
                           meals=meals,
                           recipes=picked_recipes)
    
def check_create_input_for_errors(start_day, number_days):        
    valid_days = ("Sunday", "Monday", "Tuesday", "Wednesday",
                  "Thursday", "Friday", "Saturday")
    error = None
    
    if not start_day:
        error = 'Day to start on is required.'
    elif start_day not in valid_days:
        error = 'That is not a valid day.'
    elif not number_days:
        error = 'Number of days is required.'
    return error

def combine_ingredient_lists(ingredient_names, ingredient_amounts,
                             ingredient_measurements):
    grocery_list = []
    for name, amount, measurement in zip(ingredient_names, 
                                         ingredient_amounts,
                                         ingredient_measurements):
        ingredient_info = ("%(name)s: %(amount)s %(measurement)s" % {
                "name":name, "amount":amount, "measurement":measurement})
        ingredient_info = ingredient_info.rstrip()
        grocery_list.append(ingredient_info)
    return grocery_list

# saves grocery_df to current working directory as text file
# figure out how to make this display save as dialog box to customize
# saving location
def save_as(grocery_df, picked_recipes):
    current_date = datetime.datetime.today().strftime("%Y-%m-%d")
#    test_file = open("grocerylist.txt", "a")
#    test_file.write(grocery_df.to_string())
#    test_file.close()
    filename = ("Grocery List %(date)s.txt" % {"date":current_date})
    np.savetxt(filename, grocery_df.values, fmt = "%s")
#    return send_file(test_file, as_attachment=True, attachment_filename="grocery_list.txt")
