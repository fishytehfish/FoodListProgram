# -*- coding: utf-8 -*-
"""
Created on Fri May 18 15:55:15 2018

@author: MANHARDTD
"""

#Main menu takes user input and checks against the different choices allowed

def MainMenu():
    MainMenuValidChoice = False
    while MainMenuValidChoice == False:
        MainMenuChoice = input('What would you like to do?\
                               1)Enter a recipe\
                               2)Create a food list\
                               3)Exit')
        #choice 1 would run the EnterNewRecipe function
        if MainMenuChoice == "1":
            MainMenuValidChoice = True
            EnterNewRecipe()
        elif MainMenuChoice == "2":
            MainMenuValidChoice = True
            CreateNewFoodList()
        elif MainMenuChoice == "3":
            quit()
            MainMenuValidChoice = True
        else:
            print("That was not a valid option, \
                  please enter an integer for your choice")