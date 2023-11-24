

'''
	import apoplast.shows.essential_nutrients.grove.seek as grove_seek
	protein = grove_seek.beautifully (
		grove = grove,
		for_each = lambda entry : True if "protein" in entry ["essential"] ["names"] else False
	)
'''

'''
{
	"essential": {},
	"natures": [],
	"unites": []
}
'''

'''
	# recursive
'''
import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list_scan
import apoplast.shows.essential_nutrients.DB.access as access

def beautifully (
	grove,
	for_each = lambda * p, ** k : None,
	
	story = 1
):
	for entry in grove:
		if (for_each (entry)):
			return entry
		
		if (len (entry ["unites"]) >= 1):
			grove = entry ["unites"]
		
			found = beautifully (
				grove,
				for_each = for_each,
				story = story + 1
			);
			if (type (found) == dict):
				return found;
		
		

	return None