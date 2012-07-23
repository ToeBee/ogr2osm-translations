'''
ogr2osm translation file for converting TIGER 2011 shapefiles into .osm format.

NOTE! To use this translation, you need to download the "featnames" file that ccompanies each TIGER shapefile. Then you need to join 
that file to the shapefile in QGIS or ArcMap or something based on LINEARID. This will allow for the street name abbreviations to 
be processed correctly. 

This translation file requires the new version of ogr2osm (see readme)
'''

'''import dbf

class dbfReader:
    index = None
'''
    
class lookups:
    directions = {'N':'North', 'E':'East', 'S':'South', 'W':'West', 'NE':'Northeast', 'NW':'Northwest', 'SE':'Southeast', 'SW':'Southwest'}
    streetTypes = {'Ave':'Avenue', 'Cam':'Camino', 'Way':'Way', 'Walk':'Walk', 'Ter':'Terrace', 
                   'St':'Street', 'Rd':'Road', 'Pl':'Place', 'Ln':'Lane', 'Fwy':'Freeway', 
                   'Dr':'Drive', 'Ct':'Court', 'Cir':'Circle', 'Blvd':'Boulevard', 'Aly':'Alley',
                   'Pt':'Point', 'Vis':'Vista', 'Trl':'Trail', 'Vw':'View', 'Crst':'Crest', 'Pass':'Pass',
                   'Hwy':'Highway', 'Plz':'Plaza', 'Loop':'Loop', 'Cres':'Crescent', 'Corte':'Corte', 'Via':'Via',
                   'Rue':'Rue', 'Pso':'Paseo', 'State Rte':'State Route' }

def filterTags(attrs):
    if not attrs: return

    tags = {}
    
    tags.update({'tiger:mtfcc':attrs['MTFCC']})
    tags.update({'tiger:linearid':attrs['LINEARID']})
    tags.update({'tiger:source':'TIGER 2011 ogr2osm import'})
    tags.update({'tiger:reviewed':'no'})
    
    #commented out code is an attempt to read the TIGER feature names in for processing names. For now I'm joining this to the shapefile in QGIS.
    #This may not be ideal for roads with multiple names but right now I'm just doing one section of residential roads so it should work ok. 
    '''if(dbfReader.index == None): 
        table = dbf.Table('featnames.dbf')
        print 'indexing feature names'
        dbfReader.index = table.create_index(lambda rec: rec.linearid)
        print 'done indexing'
        
    records = dbfReader.index.search(match=(attrs['LINEARID']))
    print 'found records for ' + attrs['LINEARID']
    print records '''
    
    if attrs['FULLNAME']:
        tags.update({'name':composeName(attrs)})
    
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

def composeName(attrs):
    finalName = ''
    if(attrs['PREDIRABRV']):
        finalName += safeLookup(attrs['PREDIRABRV'], lookups.directions) + ' '
    if(attrs['PRETYPABRV']):
        finalName += safeLookup(attrs['PRETYPABRV'], lookups.streetTypes) + ' '
    if(attrs['NAME']):
        finalName += attrs['NAME'] + ' '
    if(attrs['SUFTYPABRV']):
        finalName += lookups.streetTypes[attrs['SUFTYPABRV']] + ' '
    return finalName.rstrip()

def safeLookup(key, lookup):
    try:
        return lookup[key]
    except KeyError:
        print 'key not found: ' + key
        return '';

def translateDirection(abbrev):
    if abbrev == 'E':
        return 'East'
    elif abbrev == 'S':
        return 'South'
    elif abbrev == 'W':
        return 'West'
    elif abbrev == 'N':
        return 'North'

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
