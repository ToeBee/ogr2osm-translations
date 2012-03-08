"""
ogr2osm translation file I used to import all bicycle racks in the city of 
Manhattan, KS into OSM from a shapefile provided to me by the city.

This translation file requires the old version of ogr2osm (see readme)
"""

def translateAttributes(attrs):
	if not attrs: return

	tags = {}

	if attrs['Style']:
		tags.update({'MHK:Style':attrs['Style']})
	if attrs['Capacity']:
		tags.update({'capacity':attrs['Capacity'].lstrip(' ')})
	if attrs['Condition']:
		tags.update({'MHK:Condition':attrs['Condition']})
	if attrs['Owner']:
		if attrs['Owner'].find('City') != -1:
			tags.update({'operator':'City of Manhattan'})
			tags.update({'access':'yes'})
		elif attrs['Owner'].find('KSU') != -1:
			tags.update({'operator':'Kansas State University'})
			tags.update({'access':'university'})
		elif attrs['Owner'].find('RLCO') != -1:
			tags.update({'operator':'Riley County'})
			tags.update({'access':'yes'})
		else:
			tags.update({'MHK:Owner':attrs['Owner']})
	
	if attrs['Security']:
		tags.update({'MHK:Security':attrs['Security']})
	if attrs['Locking']:
		tags.update({'MHK:Locking':attrs['Locking']})
	if attrs['Weather_Pr']:
		if attrs['Weather_Pr'].find('Yes') != -1:
			tags.update({'covered':'yes'})
		elif attrs['Weather_Pr'].find('No') != -1:
			tags.update({'covered':'no'})
	if 'Notes' in attrs:
		print "Notes in attrs!"
		if attrs['Notes']:
			tags.update({'notes':attrs['Notes']})

	return tags
