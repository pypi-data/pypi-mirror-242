


'''
	returns the "mass + eq mass" in grams
'''


import apoplast.measures._interpret.unit_kind as unit_kind
import apoplast.measures.mass.swap as mass_swap
import apoplast.measures.number.decimal.reduce as reduce_decimal


from fractions import Fraction

'''

'''
def calc_food_nutrient_amount (
	USDA_food_nutrient,
	mass_and_volume,
	amount_per_portion = 100
):
	assert ("nutrient" in USDA_food_nutrient)
	assert ("name" in USDA_food_nutrient ["nutrient"])
	assert ("amount" in USDA_food_nutrient)
	name = USDA_food_nutrient ["nutrient"] ["name"]
	food_nutrient_amount = USDA_food_nutrient ["amount"]
	unit_name = USDA_food_nutrient ["nutrient"] ["unitName"]

	print (
		float (Fraction (
			mass_and_volume ["mass"]["per package"]["grams"]["fraction string"]
		)),
		float (amount_per_portion),
		float (Fraction (food_nutrient_amount))
	)
	
	mass_plus_mass_eq_per_package__from_portion = Fraction (
		Fraction (
			mass_and_volume ["mass"]["per package"]["grams"]["fraction string"]
		),
		amount_per_portion
	) * Fraction (food_nutrient_amount)
	
	return mass_plus_mass_eq_per_package__from_portion;


'''

'''
def calc_label_nutrient_amount (
	USDA_label_nutrient,
	servings_per_package
):
	assert ("value" in USDA_label_nutrient)
	USDA_label_nutrient_amount = USDA_label_nutrient ["value"]
	
	mass_plus_mass_eq_per_package__from_label = (
		Fraction (USDA_label_nutrient_amount) *
		Fraction (servings_per_package)
	)

	return mass_plus_mass_eq_per_package__from_label;

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
		

	if (mass_and_volume ["mass"]["calculated"]):
		assert ("unitName" in USDA_food_nutrient ["nutrient"])
		unit_name = USDA_food_nutrient ["nutrient"] ["unitName"]
		
		'''
			Could also be "biological activity" or "volume"
		'''
		if (unit_kind.calc (unit_name) == "mass"):
			mass_plus_mass_eq_per_package__from_portion = calc_food_nutrient_amount (
				USDA_food_nutrient,
				mass_and_volume
			)
			
			'''
			difference = abs (
				mass_plus_mass_eq_per_package__from_portion -
				label_nutrient_amount
			)
			assert (difference <= 1)
			'''
			
			if (records >= 1):
				print (
					"mass_plus_mass_eq_per_package__from_portion", 
					mass_plus_mass_eq_per_package__from_portion,
					float (mass_plus_mass_eq_per_package__from_portion)
				)
						
			
			print ("unit_name:", unit_name)
			
			mass_plus_mass_eq_per_package_in_grams = Fraction (mass_swap.start ([ 
				mass_plus_mass_eq_per_package__from_portion, 
				unit_name 
			], "grams"))
			
			return {
				"mass + mass equivalents": {
					"per package": {
						"listed": [ 
							reduce_decimal.start (
								mass_plus_mass_eq_per_package__from_portion, 
								partial_size = 3
							), 
							unit_name 
						],
						"grams": {
							"decimal string": reduce_decimal.start (
								mass_plus_mass_eq_per_package_in_grams, 
								partial_size = 3
							),
							"fraction string": str (mass_plus_mass_eq_per_package_in_grams)
						}
					}
				}
			}
			
		if (unit_kind.calc (unit_name) == "biological activity"):
			assert (unit_name.lower () == "iu")
		
			biological_activity__from_portion = calc_food_nutrient_amount (
				USDA_food_nutrient,
				mass_and_volume
			)
			
			'''
			difference = abs (
				biological_activity__from_portion -
				label_nutrient_amount
			)
			assert (difference <= 1)
			'''
			
			print ("biological_activity__from_portion:", biological_activity__from_portion)
			
			biological_activity_per_package_in_IU = Fraction (biological_activity__from_portion)
			
			return {
				"biological activity": {
					"per package": {
						"listed": [ 
							reduce_decimal.start (
								biological_activity__from_portion, 
								partial_size = 3
							), 
							unit_name 
						],
						"IU": {
							"decimal string": reduce_decimal.start (
								biological_activity_per_package_in_IU, 
								partial_size = 3
							),
							"fraction string": str (biological_activity_per_package_in_IU)
						}
					}
				}
			}
		
	return {}

