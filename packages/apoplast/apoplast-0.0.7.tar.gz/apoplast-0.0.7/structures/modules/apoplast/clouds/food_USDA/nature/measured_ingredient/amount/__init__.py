


'''
	returns the "mass + eq mass" in grams
'''


import apoplast.measures._interpret.unit_kind as unit_kind

import apoplast.clouds.food_USDA.nature.measured_ingredient.amount.calc.food_nutrient_calculator as food_nutrient_calculator
import apoplast.clouds.food_USDA.nature.measured_ingredient.amount.calc.label_nutrient_calculator as label_nutrient_calculator

import apoplast.clouds.food_USDA.nature.measured_ingredient.amount.mass as mass_calculator
import apoplast.clouds.food_USDA.nature.measured_ingredient.amount.biological_activity as biological_activity_calculator
import apoplast.clouds.food_USDA.nature.measured_ingredient.amount.energy as energy_calculator


from fractions import Fraction

def calc (
	USDA_food_nutrient,
	mass_and_volume,
	servings_per_package,

	USDA_label_nutrient = {},
	records = 1
):

	'''
		These difference assertions
		require nutrient name equivalency guessing.
	'''	
	'''
		This measure is for asserting that the 
		food nutrient measure is accurate.
	'''
	'''
	label_nutrient_amount = calc_label_nutrient_amount (
		USDA_label_nutrient,
		servings_per_package
	)
	if (records >= 1):
		print (
			"label_nutrient_amount", 
			label_nutrient_amount,
			float (label_nutrient_amount)
		)	
	'''	
		
	amount_per_package__from_portion = food_nutrient_calculator.calc (
		USDA_food_nutrient,
		mass_and_volume
	)
		
	if (mass_and_volume ["mass"]["ascertained"]):	
		assert ("unitName" in USDA_food_nutrient ["nutrient"])
		unit_name = USDA_food_nutrient ["nutrient"] ["unitName"]
		
		if (unit_kind.calc (unit_name) == "mass"):
			return mass_calculator.calc (
				amount_per_package__from_portion,
				unit_name,
				
				USDA_food_nutrient,
				mass_and_volume,
				servings_per_package,
				
				records
			)
		
			
		if (unit_kind.calc (unit_name) == "biological activity"):
			return biological_activity_calculator.calc (
				amount_per_package__from_portion,
				unit_name,
				
				USDA_food_nutrient,
				mass_and_volume,
				servings_per_package,
				
				records
			)
			
		if (unit_kind.calc (unit_name) == "energy"):		
			return energy_calculator.calc (
				amount_per_package__from_portion,
				unit_name,
				
				USDA_food_nutrient,
				mass_and_volume,
				servings_per_package,
				
				records
			)
		
	return {}

