'''
A trivial ogr2osm translation file that discards all tags.
This is useful if you only want to use the geometry of your source.

Example: using a new source of data to update admin boundary relations 
that already exist and are tagged appropriately.

@author: toby
'''
def filterTags(attrs):
    return {}