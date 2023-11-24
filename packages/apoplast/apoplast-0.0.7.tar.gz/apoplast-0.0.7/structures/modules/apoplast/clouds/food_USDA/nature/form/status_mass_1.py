




'''
	python3 insurance.py "clouds/food_USDA/nature/form/status_mass_1.py"
'''

import apoplast.clouds.food_USDA.interpret.packageWeight as package_weight
import apoplast.clouds.food_USDA.nature.form as form_builder
	
import apoplast.clouds.food_USDA.examples as USDA_examples

import json

def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	mass_and_volume = package_weight.calc (walnuts_1882785)
	
	print (mass_and_volume)

	form = form_builder.build (
		serving_size = walnuts_1882785 ["servingSize"],
		serving_size_unit = walnuts_1882785 ["servingSizeUnit"],
		mass_and_volume = mass_and_volume
	)
	servings_per_package = form.servings_per_package;
	
	assert (servings_per_package == "227/14")
	
	print (servings_per_package)

	
checks = {
	"check 1": check_1
}