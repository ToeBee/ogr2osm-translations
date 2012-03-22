'''
Translation file for washington county boundaries from the Washington State Department of Ecology.
The file I used was downloaded from here: ftp://www.ecy.wa.gov/gis_a/polsub/counties.zip

I'm just using the County_arc.shp file. It only has line geometries. One line per shared county border.
There is no name or other non-geographic data which is fine since I'm only replacing license dirty ways.
The county name and such will stay in the boundary relations which are not license tainted

All this translation file really does is add basic way tags and some source tags as required by the 
Department of Ecology here:
http://www.ecy.wa.gov/copyright.html
'''

def filterTags(attrs):
    if not attrs: return
    
    tags = {}
    
    tags.update({'boundary':'administrative'})
    tags.update({'admin_level':'6'})
    tags.update({'border_type':'county'})
    tags.update({'source':'Washington State Department of Ecology'})
    tags.update({'source:ref':'http://www.ecy.wa.gov/services/gis/data/polsub/counties.htm'})
    
    return tags
