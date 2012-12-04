'''
ogr2osm translation file for converting TIGER 2011 shapefiles into .osm format.

NOTE! To use this translation, you need to download the "featnames" file that ccompanies each TIGER shapefile. Then you need to join 
that file to the shapefile in QGIS or ArcMap or whatever, based on LINEARID. This will allow for the street name abbreviations to 
be processed correctly.

NOTE 2! To expand abbreviations, this uses the CSV file tiger2012_abrv.csv which is also in this repo. However due to the limited 
amount of information that gets passed in to the translation, I can't really know where to look for this file. So you must copy the 
csv file to your current working directory before executing ogr2osm

This translation file requires the new version of ogr2osm (see readme)
'''
import os
import csv

streetTypes = {}
directionCodes = {}
nameQualifiers = {}
    
try:
    # Codes are from the TIGER technical documentation
    directionCodes.update({'11':'North', '12':'South', '13':'East', '14':'West', '15':'Northeast', '16':'Northwest', '17':'Southeast', '18':'Southwest', 
                           '19':'Norte', '20':'Sur', '21':'Este', '22':'Oeste', '23':'Noreste', '24':'Noroeste', '25':'Sudeste', '26':'Sudoeste'})
    nameQualifiers.update({'11':'Access', '12':'Alternate', '13':'Business', '14':'Bypass', '15':'Connector', '16':'Extended', '17':'Extension', '18':'Historic', 
                           '19':'Loop', '20':'Old', '21':'Private', '22':'Public', '23':'Scenic', '24':'Spur', '25':'Ramp', '26':'Underpass', '27':'Overpass'})
    print "reading abbreviation CSV file"
    f = open('tiger2012_abbrv.csv', 'rb')
    abbrevReader = csv.reader(f, delimiter=',')
    for row in abbrevReader:
        streetTypes[row[0]] = row[1]
        
    print "Read tiger abbreviations: " + str(len(streetTypes))
except:
    print "\n\nError reading TIGER abbreviations. This will lead to bad data! Exiting." 
    print "Please read the comments at the top of this translation regarding the abbreviations file\n\n"
    os._exit()

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
    elif attrs['MTFCC'] == 'S1750' and attrs['FULLNAME'] == 'Driveway':
        del tags['name']
    elif attrs['MTFCC'] == 'S1780':
        tags.update({'service':'parking_aisle'})
    
    return tags

def composeName(attrs):
    finalName = ''
    if(attrs['PREQUAL']):
        finalName += nameQualifiers[attrs['PREQUAL']] + ' '
    if(attrs['PREDIR']):
        finalName += directionCodes[attrs['PREDIR']] + ' '
    if(attrs['PRETYP']):
        finalName += streetTypes[attrs['PRETYP']] + ' '
    if(attrs['NAME']):
        finalName += attrs['NAME'] + ' '
    if(attrs['SUFTYP']):
        finalName += streetTypes[attrs['SUFTYP']] + ' '
    if(attrs['SUFDIR']):
        finalName += directionCodes[attrs['SUFDIR']] + ' '
    if(attrs['SUFQUAL']):
        finalName += nameQualifiers[attrs['SUFQUAL']] + ' '
    return finalName.rstrip()

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
    elif mtfcc == 'S1750':
        return 'service'
    elif mtfcc == 'S1780':
        return 'service'
    elif mtfcc == 'S1820':
        return 'cycleway'
    elif mtfcc == 'S1830':
        return 'bridleway'
    else:
        return 'road'
