
'''
	python3 insurance.py shows/essential_nutrients/grove/measures/add/status_1.py
'''

import apoplast.shows.essential_nutrients.grove.measures.add as add_grove_measures
	
import json	
	
def check_1 ():
	entry = {
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
		"measures": {},
		"natures": [],
		"unites": []
	}

	add_grove_measures.beautifully (
		entry = entry,
		source = {
			"name":	"WALNUTS HALVES & PIECES, WALNUTS",
			"FDC ID": "1882785",
			"UPC": "099482434618",
			"DSLD ID": ""
		},
		measured_ingredient = {
			"name": "Potassium, K",
			"measures": {
				"mass + mass equivalents": {
					"per package": {
						"listed": [
							"1947.660",
							"mg"
						],
						"grams": {
							"decimal string": "1.948",
							"fraction string": "97383/50000"
						}
					}
				}
			}
		}
	)
	
	print (json.dumps (entry, indent = 4))

	assert (
		entry ["natures"] ==
		[
			{
				"source": {
					"name": "WALNUTS HALVES & PIECES, WALNUTS",
					"FDC ID": "1882785",
					"UPC": "099482434618",
					"DSLD ID": ""
				},
				"ingredient": {
					"name": "Potassium, K"
				},
				"measures": {
					"mass + mass equivalents": {
						"per package": {
							"listed": [
								"1947.660",
								"mg"
							],
							"grams": {
								"decimal string": "1.948",
								"fraction string": "97383/50000"
							}
						}
					}
				}
			}
		]
	)
	
	assert (
		entry ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": "97383/50000"
					}
				}
			}
		}
	)

	return;
	
	
checks = {
	'check 1': check_1
}