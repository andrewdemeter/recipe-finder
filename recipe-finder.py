import requests
from operator import itemgetter

# Set API keys
api_ninjas_key = ""
spoonacular_key = ""

# User enters their available ingredients
ingredients = input("Please enter the ingredients you have...\n")

# Set headers for first API call
headers = {
    'X-Api-Key': api_ninjas_key
}

# Call the API Ninjas /nutrition endpoint, which will extract ingredients from the user's input
response = requests.request("GET", "https://api.api-ninjas.com/v1/nutrition?query=" + ingredients, headers=headers)
extracted_ingredients = response.json()

# Create an empty list, which will store the extracted ingredients
ingredient_list = []

# Loop through each extracted ingredient and add it to the ingredient list
for ingredient in extracted_ingredients:
    ingredient_list.append(ingredient['name'])

# Format the ingredient list as a comma-separated string so it can be used in the next request
ingredient_list_string = ",".join(ingredient_list)

# Set headers for the second API call
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Call the Spoonacular /recipes/findByIngredients endpoint, which will return the 10 most relevant recipes
response = requests.request("GET", "https://api.spoonacular.com/recipes/findByIngredients?apiKey=" + spoonacular_key + "&ingredients=" + ingredient_list_string + "&ignorePantry=true")
unsorted_recipes = response.json()

# Sort the 10 recipes by number of missing ingredients in ascending order
sorted_recipes = sorted(unsorted_recipes, key=itemgetter('missedIngredientCount'), reverse=False)

# Create an empty list, which will store the recipe IDs
recipe_id_list = []

# Loop through each recipe ID and add it to the recipe ID list
for recipe_id in sorted_recipes:
    recipe_id_list.append(str(recipe_id['id']))

# Format the recipe ID list as a comma-separated string so it can be used in the next request
recipe_id_list_string = ",".join(recipe_id_list)

# Call the Spoonacular /recipes/informationBulk endpoint, which will return the URL for each recipe
response = requests.request("GET", "https://api.spoonacular.com/recipes/informationBulk?apiKey=" + spoonacular_key + "&ids=" + recipe_id_list_string, headers=headers)
recipe_urls = response.json()

# Set the recipe index to 0
index = 0

# While the user hasn't seen all 10 recipes...
while index < 10:
    print("\nYour recommended recipe is: " + sorted_recipes[index]['title'])
    print("Click here to view it: " + recipe_urls[index]['sourceUrl'])

    if sorted_recipes[index]['usedIngredientCount'] == 1:
        print("\nThis recipe uses the following ingredient from your kitchen:")
    else:
        print("\nThis recipe uses the following ingredients from your kitchen:")

    # Iterate through and print each used ingredient
    for used_ingredient in sorted_recipes[index]['usedIngredients']:
        print("• " + used_ingredient['name'])

    if sorted_recipes[index]['missedIngredientCount'] == 0:
        print("\nYou have all the required ingredients!")
    elif sorted_recipes[index]['missedIngredientCount'] == 1:
        print("\nYou're only missing the following ingredient:")
    else:
        print("\nYou're missing the following ingredients:")

    # Iterate through and print each missing ingredient
    for missing_ingredient in sorted_recipes[index]['missedIngredients']:
        print("• " + missing_ingredient['name'])

    # Prompt the user to view the next recipe or close the program
    user_choice = input("\nType NEXT to try a different recipe, or type END to close this program.\n")

    # If the user doesn't type NEXT or END...
    while user_choice.upper() != "NEXT" and user_choice.upper() != "END":
        user_choice = input("Please type NEXT or END...\n")

    # If the user types NEXT, continue looping and fetch a new recipe
    if user_choice.upper() == "NEXT":
        index += 1

    # If the user types END, quit the program
    if user_choice.upper() == "END":
        quit()

# Inform the user that they have cycled through all 10 recipes
print("You've seen all 10 recipes! Restart this program to try other ingredients.")