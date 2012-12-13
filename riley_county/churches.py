'''
Translation file to convert the Riley County churches shpaefile to OSM format.

The shapefile contains 76 points. Where possible, building outlines will be traced 
from imagery and the tags added to the outline.

Tag translation
The shapefile contains NAME, ADDRESS, CITY and PHONENM. 

NAME -> name
A couple names need a little cleaning up because they contain things like the 
denomination's district name and such.

ADDRESS -> addr:housenumber, addr:street based on a regular expression.
If the record does not contain a specific street address, it is not converted to tags.
Street names are unabbreviated. A few directional prefixes need to be expanded by hand
 
CITY -> addr:city where available
 
PHONENM -> phone where available. Format is 785-555-1234

religion and denomination tags will be added manually where 
it is obvious from the name or known from another source
'''
import re

def filterTags(attrs):
    if not attrs: return

    tags = {}
    
    tags.update({'amenity':'place_of_worship'})
    tags.update({'source':'Riley County GIS'})
    tags.update({'name':attrs['NAME']})
    tags.update({'phone':attrs['PHONENM']})
    if(attrs['CITY']):
        tags.update({'addr:city':attrs['CITY']})
        
    match = re.match("(\d+) (.*)", attrs['ADDRESS'])
    if(match):
        tags.update({'addr:housenumber':match.group(1)})
        tags.update({'addr:street':match.group(2)})
    
    
    return tags;