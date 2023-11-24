
'''
import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
build_essential_nutrients_land.eloquently ()
'''

'''
	plan:
		1. 	build the grove of essential nutrients 
			from the essential nutrients DB
		
		2. 
'''

import apoplast.shows.essential_nutrients.grove.nurture as grove_nurture
	
def eloquently ():
	structure = {
		"measures": {
			"mass + mass equivalents": {
				"per package": {
					"grams": {
						"decimal string": "",
						"fraction string": ""
					}
				}
			},
			"biological activity": {
				"per package": {
					"IU": {
						"decimal string": "",
						"fraction string": ""
					}
				}
			},
			"energy": {
				"per package": {
					"calories": {
						"decimal string": "",
						"fraction string": ""
					},
					"joules": {
						"decimal string": "",
						"fraction string": ""
					}
				}
			}
		},
		"grove": grove_nurture.beautifully (),
		"exclusions": []
	}

	return structure