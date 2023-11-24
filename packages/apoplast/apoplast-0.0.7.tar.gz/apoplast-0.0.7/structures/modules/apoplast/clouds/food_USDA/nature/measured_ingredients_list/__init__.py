

import apoplast.clouds.food_USDA.nature.measured_ingredient as measured_ingredient_builder
#measured_ingredient_builder.build ()

def build (
	food_USDA,
	mass_and_volume,
	servings_per_package,
	
	records = 0
):
	assert ("foodNutrients" in food_USDA)

	measured_ingredients_list = []

	food_nutrients = food_USDA ["foodNutrients"]
	for USDA_food_nutrient in food_nutrients:
		measured_ingredient = measured_ingredient_builder.build (
			USDA_food_nutrient,
			mass_and_volume,
			servings_per_package,
			
			records = 0
		)
	
		measured_ingredients_list.append (measured_ingredient)

	#import json
	#print (json.dumps (measured_ingredients_list, indent = 4))
	
	'''
		From the list, structure the list based on the essential nutrients DB.
	'''
	
	
		
		
	return measured_ingredients_list