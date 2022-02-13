import requests
from operator import itemgetter

# Set API keys
api_ninjas_key = ""
spoonacular_key = ""

# User enters their available ingredients
ingredients = input("Please enter your ingredients...\n")

# User enters their preference
preference = input("Type 1 to find recipes that use up as many of your ingredients as possible.\n"
                   "Type 2 to find recipes that require the fewest additional ingredients.\n")

# If the user doesn't enter 1 or 2...
while preference != "1" and preference != "2":
    preference = input("Please enter 1 or 2 to continue...\n")

# Set headers for the API Ninjas request
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

# Call the Spoonacular /recipes/findByIngredients endpoint, which will return a maximum of 10 relevant recipes
response = requests.request("GET", "https://api.spoonacular.com/recipes/findByIngredients?apiKey=" + spoonacular_key +
                            "&ingredients=" + ingredient_list_string + "&ranking=1&ignorePantry=true")
recipes = response.json()

# If the user prefers recipes that require the fewest additional ingredients
if preference == "2":
    # Sort the returned recipes by number of missing ingredients in ascending order
    recipes = sorted(recipes, key=itemgetter('missedIngredientCount'), reverse=False)

# Create an empty list, which will store the recipe IDs
recipe_id_list = []

# Loop through each recipe ID and add it to the recipe ID list
for recipe_id in recipes:
    recipe_id_list.append(str(recipe_id['id']))

# Format the recipe ID list as a comma-separated string so it can be used in the next request
recipe_id_list_string = ",".join(recipe_id_list)

# Call the Spoonacular /recipes/informationBulk endpoint, which will return the URL for each recipe
response = requests.request("GET", "https://api.spoonacular.com/recipes/informationBulk?apiKey=" + spoonacular_key +
                            "&ids=" + recipe_id_list_string)
recipe_urls = response.json()

# Set the recipe index to 0
index = 0

# Set the number of returned recipes (maximum of 10)
total_recipes = len(recipe_id_list)

# If no recipes were returned, inform the user
if total_recipes == 0:
    print("No recipes were found based on the provided ingredients. Please try again.")
    quit()

# While the user hasn't seen all the returned recipes...
while index < total_recipes:
    print("\nYour recommended recipe is: " + recipes[index]['title'])
    print("Click here to view it: " + recipe_urls[index]['sourceUrl'])

    if recipes[index]['usedIngredientCount'] == 1:
        print("\nThis recipe uses the following ingredient from your kitchen:")
    else:
        print("\nThis recipe uses the following ingredients from your kitchen:")

    # Iterate through and print each used ingredient
    for used_ingredient in recipes[index]['usedIngredients']:
        print("• " + used_ingredient['name'])

    if recipes[index]['missedIngredientCount'] == 0:
        print("\nYou have all the required ingredients!")
    elif recipes[index]['missedIngredientCount'] == 1:
        print("\nYou're only missing the following ingredient:")
    else:
        print("\nYou're missing the following ingredients:")

    # Iterate through and print each missing ingredient
    for missing_ingredient in recipes[index]['missedIngredients']:
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

# Inform the user that they have cycled through all the returned recipes
print("You've seen all the recipes! Restart this program to try other ingredients.")
