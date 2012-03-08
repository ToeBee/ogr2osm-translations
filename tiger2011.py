'''
ogr2osm translation file for converting TIGER 2011 shapefiles into .osm format.

This translation file requires the new version of ogr2osm (see readme)
'''

def filterTags(attrs):
    if not attrs: return

    tags = {}
    
    tags.update({'tiger:mtfcc':attrs['MTFCC']})
    tags.update({'tiger:linearid':attrs['LINEARID']})
    tags.update({'tiger:source':'TIGER 2011 ogr2osm import'})
    tags.update({'tiger:reviewed':'no'})
    if attrs['FULLNAME']:
        tags.update({'name':attrs['FULLNAME']})
    
    tags.update({'highway':mtfccToHighway(attrs['MTFCC'])})
    
    if attrs['MTFCC'] == 'S1100':
        tags.update({'oneway':'yes'})
    elif attrs['MTFCC'] == 'S1630':
        tags.update({'oneway':'yes'})
    elif attrs['MTFCC'] == 'S1730':
        tags.update({'service':'alley'})
    elif attrs['MTFCC'] == 'S1740':
        tags.update({'access':'private'})
    elif attrs['MTFCC'] == 'S1780':
        tags.update({'service':'parking_aisle'})
    
    return tags


def mtfccToHighway(mtfcc):
    if mtfcc == 'S1100':
        return 'motorway'
    elif mtfcc == 'S1200':
        return 'primary'
    elif mtfcc == 'S1300':
        return 'tertiary'
    elif mtfcc == 'S1400':
        return 'residential'
    elif mtfcc == 'S1500':
        return 'track'
    elif mtfcc == 'S1630':
        return 'service'
    elif mtfcc == 'S1640':
        return 'service'
    elif mtfcc == 'S1710':
        return 'footway'
    elif mtfcc == 'S1720':
        return 'steps'
    elif mtfcc == 'S1730':
        return 'service'
    elif mtfcc == 'S1740':
        return 'service'
    elif mtfcc == 'S1780':
        return 'service'
    elif mtfcc == 'S1820':
        return 'cycleway'
    elif mtfcc == 'S1830':
        return 'bridleway'
    else:
        return 'road'
