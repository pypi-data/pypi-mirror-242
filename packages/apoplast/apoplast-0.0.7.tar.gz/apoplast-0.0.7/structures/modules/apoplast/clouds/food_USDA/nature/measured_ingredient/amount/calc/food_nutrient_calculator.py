
'''
import apoplast.measures._interpret.unit_kind as unit_kind
import apoplast.measures.mass.swap as mass_swap
import apoplast.measures.number.decimal.reduce as reduce_decimal
import apoplast.measures.energy.swap as energy_swap
'''

from fractions import Fraction

'''

'''
def calc (
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

	'''
	print (
		float (Fraction (
			mass_and_volume ["mass"]["per package"]["grams"]["fraction string"]
		)),
		float (amount_per_portion),
		float (Fraction (food_nutrient_amount))
	)
	'''
	
	mass_plus_mass_eq_per_package__from_portion = Fraction (
		Fraction (
			mass_and_volume ["mass"]["per package"]["grams"]["fraction string"]
		),
		amount_per_portion
	) * Fraction (food_nutrient_amount)
	
	return mass_plus_mass_eq_per_package__from_portion;