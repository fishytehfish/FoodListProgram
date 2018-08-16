# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 20:23:34 2018

@author: David
"""

# takes final dataframe with recipes for each meal, and reads each recipes ingredients, outputs grocery list as text file with
# today's date in name

def create_grocery_list(final_recipe_dataframe):
    all_recipes = []
    for recipe in final_recipe_dataframe.itertuples():
        all_recipes.append(recipe.Breakfast)
        all_recipes.append(recipe.Lunch)
        all_recipes.append(recipe.Dinner)
        # create count for each unique recipe in each list
        for recipe in all_recipes:
            servings_needed = all_recipes.count(recipe)
            print(("%(recipe)s needs %(serving)s servings") % {
                    "recipe":recipe, "serving":servings_needed})
        # read ingredient info for each unique recipe
            recipe_information = read_recipe_information(recipe_name=recipe)
            print("recipe serving size = %(size)s") % {"size":recipe_serving_size}
        # if the count for each recipe is different from the serving size
            #if servings_needed != recipe_serving_size:
            # then change each ingredient amount by that amount
            
        # add ingredients to grocery list
        
        # check to see if ingredient is already in grocery list
        # if it is, then check if measurement is the same
        # convert measurement if necessary
        
        # output final grocery list