
'''
	import apoplast.clouds.food_USDA.nature.form as form_builder
	form_builder.build ()
'''

'''
	"Servings per package" is necessary for calculating the "per package"
	"mass + mass equivalents", "mass", ior "volume" of a measured ingredient.
'''

'''
"serving size": {
	"mass": {
		"grams": {
			"fraction string": str (Fraction (food_USDA ["servingSize"]))
		}
	}
},
"servings per package": ""
'''

from fractions import Fraction

import apoplast.measures._interpret.unit_kind as unit_kind
import apoplast.measures.volume.swap as volume_swap
import apoplast.measures.mass.swap as mass_swap

def build (
	serving_size,
	serving_size_unit,
	mass_and_volume,
	
	records = 1
):
	serving_size = Fraction (serving_size)
	serving_size_unit_kind = unit_kind.calc (serving_size_unit)

	if (records >= 1):
		print ("serving_size_unit_kind =", serving_size_unit_kind)

	if (serving_size_unit_kind == "mass"):	
		serving_size_mass_in_grams = mass_swap.start ([ serving_size, serving_size_unit ], "grams")
		package_mass_in_grams = Fraction (mass_and_volume ["mass"] ["per package"] ["grams"] ["fraction string"])

		servings_per_package = Fraction (
			package_mass_in_grams,
			serving_size_mass_in_grams
		)
		
		class Proceeds:
			servings_per_package = ""
			
		proceeds = Proceeds ()
		proceeds.servings_per_package = str (servings_per_package)
		proceeds.package_mass_in_grams = str (package_mass_in_grams)
			
		return proceeds;

	elif (serving_size_unit_kind == "volume"):	
		serving_size_volume_in_liters = volume_swap.start ([ serving_size, serving_size_unit ], "liters")
		package_volume_in_liters = Fraction (mass_and_volume ["volume"] ["per package"] ["liters"] ["fraction string"])
		
		servings_per_package = Fraction (
			package_volume_in_liters,
			serving_size_volume_in_liters
		)
		
		class Proceeds:
			servings_per_package = ""
			
		proceeds = Proceeds ()
		proceeds.servings_per_package = str (servings_per_package)
		proceeds.package_volume_in_liters = str (package_volume_in_liters)
			
		return proceeds;
	

	return;