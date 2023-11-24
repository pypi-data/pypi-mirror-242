


"""
	essentials nutrients grove
"""

'''
	priorities:
		steps:
			1.  build the essential nutrients structure
			
			2.  loop through the measured ingredient list and
				merge any essentials found into the essential 
				nutrients structure.grove

					if an ingredient is not found in the ENSG, 
					then raise an alarm about it.
'''

import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
import apoplast.shows.essential_nutrients.grove.seek as grove_seek
import json	
	
def seek_measured_ingredient_name (
	measured_ingredient_name = "",
	grove = []
):
	checked = []
	def for_each (entry):		
		accepts = []
		if ("accepts" in entry ["essential"]):
			accepts = entry ["essential"] ["accepts"]
	
		patterns = [
			* entry ["essential"] ["names"],
			* accepts
		]	
		
		checked.append (patterns)
			
		for name in patterns:
			if (measured_ingredient_name == name.lower ().strip ()):
				#print (f"name: '{ name.lower ().strip () }'")
			
				return True;
			
		return False

	entry = grove_seek.beautifully (
		grove = grove,
		for_each = for_each
	)
	if (type (entry) != dict):
		print (entry)
		#print (checked)
		raise Exception ("A measured ingredient was not found.")

	return entry
	
def eloquently (
	measured_ingredients_list = [],
	identity = {}
):
	land = build_essential_nutrients_land.eloquently ()
	grove = land ["grove"]

	for measured_ingredient in measured_ingredients_list:
		measured_ingredient_name = measured_ingredient ["name"].lower ().strip ()
	
		print (f"measured_ingredient_name: '{ measured_ingredient_name }'")
		
		entry = seek_measured_ingredient_name (
			measured_ingredient_name,
			grove
		)
		
		print (json.dumps ({
			"measured_ingredient": measured_ingredient,
			"entry": entry
		}, indent = 4))
		
		#return;

	return land;