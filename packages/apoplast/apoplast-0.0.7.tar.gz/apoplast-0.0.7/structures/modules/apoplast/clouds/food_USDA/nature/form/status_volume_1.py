




'''
	python3 insurance.py "clouds/food_USDA/nature/form/status_volume_1.py"
'''

import apoplast.clouds.food_USDA.interpret.packageWeight as package_weight
import apoplast.clouds.food_USDA.nature.form as form_builder
	
import apoplast.clouds.food_USDA.examples as USDA_examples

import json

def check_1 ():
	beet_juice_2412474 = USDA_examples.retrieve ("branded/beet_juice_2412474.JSON")
	mass_and_volume = package_weight.calc (beet_juice_2412474)
	
	print (mass_and_volume)

	form = form_builder.build (
		serving_size = beet_juice_2412474 ["servingSize"],
		serving_size_unit = beet_juice_2412474 ["servingSizeUnit"],
		mass_and_volume = mass_and_volume
	)
	
	servings_per_package = form.servings_per_package;
	
	print (servings_per_package)
	assert (servings_per_package == "473/240")
	
checks = {
	"check 1": check_1
}