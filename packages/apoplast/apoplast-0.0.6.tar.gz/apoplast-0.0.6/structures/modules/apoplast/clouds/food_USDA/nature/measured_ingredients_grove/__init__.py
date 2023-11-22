

import apoplast.clouds.food_USDA.nature.measured_ingredient as measured_ingredient_builder
#measured_ingredient_builder.build ()

def build (
	food_USDA,
	mass_and_volume,
	servings_per_package
):
	assert ("foodNutrients" in food_USDA)

	measured_ingredients_list = []

	food_nutrients = food_USDA ["foodNutrients"]
	for nutrient in food_nutrients:
		measured_ingredient = {}
	
		measured_ingredients_list.append (measured_ingredient)
	
		pass;
		
	return;