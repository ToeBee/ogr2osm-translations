'''
Translation to convert the Riley county parks shapefile to OSM format.

The geometries are sometimes split in odd ways so I will be doing some manual work to merge them into appropriate areas for OSM purposes.
Some shapes are over-noded. I will simplify using JOSM's simplification tool.
Some of the parks are already mapped so I will be doing manual conflation for each park.

Attribute to OSM tag mapping is as follows:
Available attributes are: NAME, PHONENM, OWNERSHIP and ADDRESS.
NAME -> name
PHONENM -> phone
        This is a 10 digit phone number associated with the park. Typically used to reserve park or report a problem. 
OWNERSHIP -> operator
        This indicates the entity responsible for the park. Values include "Federal" "State of Kansas" "Riley County" and "City of <name>"
ADDRESS -> addr:housenumber/addr:street
        It is only an actual street address in 10 cases. These will be translated to addr:* keys.
        The rest are general location descriptions like "Yuma St & 10th St" and will be discarded.
        Street names have abbreviations in them but I will expand them by hand.
'''
import re

def filterTags(attrs):
    if not attrs: return

    tags = {}
    
    tags.update({'leisure':'park'})
    tags.update({'source':'Riley County GIS'})
    tags.update({'name':attrs['NAME']})
    tags.update({'phone':attrs['PHONENM']})
    tags.update({'operator':attrs['OWNERSHIP']})
    match = re.match("(\d+) (.*)", attrs['ADDRESS'])
    if(match):
        tags.update({'addr:housenumber':match.group(1)})
        tags.update({'addr:street':match.group(2)})
    return tags;