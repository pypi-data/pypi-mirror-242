


'''
	import apoplast.shows.essential_nutrients.grove.measures.add as grove_measures
	add_grove_measures.beautifully (
		entry,
		measured_ingredient
	)
'''

'''
	 {
		"essential": {
			"includes": [],
			"names": [
				"potassium",
				"potassium K",
				"potassium, K",
				"K"
			],
			"region": 58
		},
		
		#
		#	add to these values
		#
		#		per package -> per recipe
		#
		"measures": {
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"decimal string": "1.948",
						"fraction string": "97383/50000"
					}
				}
			}
		},
		
		#
		#	append this
		#
		"natures": [{
			"source": {
				"name": "",
				"UPC": "",
				"DSLD ID": "",
				"FDC ID": ""
			},
			"ingredient": {
				"name": "vitamin b",
			},
			"measures": {
				"mass + mass equivalents": {
					"per package": {
						"grams": {
							"decimal string": "",
							"fraction string": ""
						}
					}
				}
			}
		}],
		"unites": []
	}
'''

import copy
from fractions import Fraction

def beautifully (
	entry = {},
	source = {},
	measured_ingredient = {}
):
	entry ["natures"].append ({
		"source": copy.deepcopy (source),
		"ingredient": {
			"name": measured_ingredient ["name"]
		},
		"measures": copy.deepcopy (measured_ingredient ["measures"])
	})
	
	essential_nutrient_measures = entry ["measures"]
	
	'''
		aggregate the measures
	'''
	measured_ingredient_measures = copy.deepcopy (measured_ingredient ["measures"])
	for measure in measured_ingredient_measures:
		if (measure not in essential_nutrient_measures):
			if (measure == "mass + mass equivalents"):
				essential_nutrient_measures [ measure ] = {
					"per recipe": {
						"grams": {
							"fraction string": "0"
						}
					}
				}
		
			else:
				raise Exception (f"Measure: '{ measure }' was not accounted for.") 
		
		#
		# after inital setup
		#
		if (measure == "mass + mass equivalents"):
			current = Fraction (essential_nutrient_measures [measure]["per recipe"]["grams"]["fraction string"])
			
			essential_nutrient_measures [measure]["per recipe"]["grams"]["fraction string"] = str (
				current +
				Fraction (
					measured_ingredient_measures [measure]["per package"]["grams"]["fraction string"]
				)
			)
		
		print ("measure not found:", measure)

	return;