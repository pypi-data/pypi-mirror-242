

'''
	Details about this can be found in "apoplast.shows.nature".
'''

'''
	limitations:
		1. 	The structure of the measured ingredients 
			is not given by the API.
			
			This is different from the NIH API, where the 
			structure of the measured ingredients is
			given.
'''

'''
	#
	#	This retrieves a food's data from USDA.	
	#
	import apoplast.clouds.food_USDA.deliveries.one as retrieve_1_food
	food_USDA = retrieve_1_food.presently ()
	
	#
	#	This parses USDA foods into the nature format.
	#
	#		This should use the shared:
	#			apoplast.shows.natures
	#
	import apoplast.clouds.food_USDA.nature as food_USDA_nature
	nature = food_USDA_nature.create (food_USDA)
'''

'''
	This calculates the "defined" section of the "nature".
	
	Defined has common fields that are shared between 
	foods and supplements.
	
	From these common fields, then the "nature" "calculated"
	section can be calculated.
'''

import apoplast.shows.natures.assertions as natures_assertions

import apoplast.clouds.food_USDA.interpret.packageWeight as package_weight
import apoplast.clouds.food_USDA.interpret.packageWeight.assertions as package_weight_assertions

import apoplast.clouds.food_USDA.nature.form as recommendation_builder
import apoplast.clouds.food_USDA.nature.measured_ingredients_list as measured_ingredients_list_builder
import apoplast.clouds.food_USDA.nature.measured_ingredients_list.seek as mil_seek

import apoplast.clouds.food_USDA.nature.essential_nutrients as calculate_essential_nutrients


from fractions import Fraction

def create (
	food_USDA,
	
	return_measured_ingredients_list = False
):
	include_ounces = False
	include_grams = True

	nature = {
		"kind": "food",
		"identity": {
			"name":	food_USDA ["description"],
			"FDC ID": str (food_USDA ["fdcId"]),
			"UPC": food_USDA ["gtinUpc"],
			"DSLD ID": ""
		},
		"brand": {
			"name":	food_USDA ["brandName"],
			"owner": food_USDA ["brandOwner"]
		},
		"measures": {
			"form": {
				"serving size": {
					"grams": {
						"fraction string": str (Fraction (food_USDA ["servingSize"]))
					}
				},
				"servings per package": ""
			},
			"energy": {
				"ascertained": False,
				"per package": {}
			}
		}
	}
	
	'''
		"servings": {
			"per package": "",
			"size": {
				"grams: ""
			}
		}
	'''
	
	'''
		Most like there are going to be times
		when this isn't a SI unit.
	'''
	# print ("serving size unit:", food_USDA ["servingSizeUnit"])

	mass_and_volume = package_weight.calc (food_USDA);
	form = recommendation_builder.build (
		serving_size = food_USDA ["servingSize"],
		serving_size_unit = food_USDA ["servingSizeUnit"],
		mass_and_volume = mass_and_volume
	);
	servings_per_package = form.servings_per_package;
	
		
	#print ("mass and volume", mass_and_volume)
	
	'''
		Neither of these are necessary
		for the recipe calculations,
		since supplements don't always
		have these.
	'''
	volume = mass_and_volume ["volume"]
	mass = mass_and_volume ["mass"]
	
	nature ["measures"]["mass"] = mass
	nature ["measures"]["volume"] = volume
	
	
	measured_ingredients_list = measured_ingredients_list_builder.build (
		food_USDA,
		mass_and_volume,
		servings_per_package,
		
		records = 0
	)
	
	if (return_measured_ingredients_list):
		return measured_ingredients_list
	
	'''
		Extract the "energy" or "calories" from the measured_ingredients_list
		and "energy" to the "measured" section.
	'''
	energy = mil_seek.start ("energy", measured_ingredients_list)
	assert (type (energy) == dict), energy
	measured_ingredients_list.remove (energy)
	
	nature ["measures"]["energy"]["ascertained"] = True
	nature ["measures"]["energy"]["per package"] = energy ["measures"]["energy"]["per package"]
	assert (type (nature ["measures"]["energy"]) == dict)
	
	
	'''
		essential nutrients grove steps:
		
			1. build an "essential nutrients grove"
			2. for each nutrient, 			
	'''	
	nature ["essential nutrients"] = calculate_essential_nutrients.eloquently (
		measured_ingredients_list,
		identity = nature ["identity"]
	)
	
	'''
		make the generic assertions about the "nature"
	'''
	natures_assertions.start (nature)
	return nature
	
	
	
	
'''

'''