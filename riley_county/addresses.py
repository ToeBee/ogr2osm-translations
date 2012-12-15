'''
Translation file to convert Riley county address points to OSM format.

The shapefile contains 22,574 points that are centered over buildings. The format of the 
address data is not entirely homogeneous. Addresses in most of the county is split into 
fields indicating prefix, name and road type which can be looked up to compose the full and
unabbreviated name. Addresses within the city of Manhattan are unfortunately not split out 
so the address must be parsed out of the FULL_ADDR field instead.

Other peculiarities:
- There is inconsistent data. Most street names are all caps and abbreviated. But there are 
  a few that are unabbreviated and have mixed cases. This creates some duplication in the 
  streetType dictionary.
- Apartments are awkward. Each apartment has its own node. They are spread out in a line leading 
  away from the road they are associated with. These are tagged with a FIXME tag for manual review 
  and consolidation.
- Trailer parks have points with nothing but a number in the FULL_ADDR field. No street names. These 
  are also flagged with a FIXME for further review.
- There are a few just plain odd values like "Null Number" and entries without housenumbers and such.
  These are flagged for review with a FIXME tag.
  
In addition to the FIXME tags, more processing will be needed to conflate the data with what is
already mapped in the area.
'''
import re

directionPrefixes = {'N':'North', 'S':'South', 'E':'East', 'W':'West'}
streetType = {'AVE':'Avenue', 'BLVD':'Boulevard', 'BR':'Branch', 'BYP':'Bypass',
              'CIR':'Circle', 'CT':'Court', 'DR':'Drive', 'HILL':'Hill', 'HL':'Hill',
              'LN':'Lane', 'LNDG':'Landing', 'PEAK':'Peak', 'PL':'Place', 'RD':'Road',
              'RDG':'Ridge', 'RUN':'Run', 'SPUR':'Spur', 'ST':'Street', 'TER':'Terrace', 
              'TRL':'Trail', 'VW':'View', 'HTS':'Heights', 'PARKWAY':'Parkway', 'ALLEY':'Alley', 
              'WAY':'Way', 'ALY':'Alley', 'MILL':'Mill', 'HEIGHTS':'Heights', 'REACH':'Reach', 
              'LANDING':'Landing', 'POINT':'Point', 'PASS':'Pass', 'SQ':'Square', 'MEADOWS':'Meadows', 'PLZ':'Plaza',
              'STAIR':'Stair', 'RIDGE':'Ridge','PLAZA':'Plaza', 'VALLEY':'Valley',
              'PARK':'Park', 'Plz':'Plaza',
              #Obvious data errors or inconsistencies:
              'Ct':'Court', 'Dr':'Drive', 'P:':'Place', 'DrR':'Drive', 'DR35':'Drive','Rd':'Road',
              'St':'Street','PRKWAY':'Parkway', 'PRKWY':'Parkway', 'Blvd':'Boulevard', 'Pl':'Place'
              }

def filterTags(attrs):
    if not attrs: return
    
    tags = {}
    
    #if ADDR_NUM is present, this means that the address is split into fields
    #and we can piece it together from individual fields.
    if(attrs['ADDR_NUM']):
        tags.update({'addr:street':composeStreetName(attrs)})
        tags.update({'addr:housenumber':attrs['ADDR_NUM']})
    else: #Address not split into fields. Have to parse from the FULL_ADDR field instead
        parsedTags = parseAddress(attrs['FULL_ADDR'])
        if(parsedTags):
            tags.update(parsedTags)
    
    #County addresses have their zip code in ZIP_CODE but Manhattan addresses have it in "MANHATTAN"
    if(attrs['ZIP_CODE']):
        tags.update({'addr:postcode':attrs['ZIP_CODE']})
    if(attrs['MANHATTAN']): 
        tags.update({'addr:postcode':attrs['MANHATTAN']})

    #All parsing has failed. Slap the unprocessed FULL_ADDR value into a tag and flag with FIXME
    if(not tags):
        tags.update({'FIXME':'Unknown problem. No tags'})
        tags.update({'addr:full':attrs['FULL_ADDR']})
    
    print 'returning tags'
    return tags

def composeStreetName(attrs):
    name = ""
    if(attrs['PRE_DIR']):
        name = directionPrefixes[attrs['PRE_DIR']] + ' '
    if(attrs['PREFIX']):
        name += attrs['PREFIX'] + ' '
    name += attrs['STREET_NAM'].title() + ' '
    if(attrs['TYPE']):
        name += streetType[attrs['TYPE']]
    return name.rstrip()

def parseAddress(fullAddress):
    tags = {}
    print 'parsing address: ' + fullAddress
    
    #There are a few addresses with odd punctuation in them. Flag for manual review
    if(fullAddress.find('?') + fullAddress.find('.') != -2):
        tags.update({'addr:full':fullAddress})
        tags.update({'FIXME':'punctuation mark in name'})
        return tags
    #There are several entries like "<address 1> OR <address 2>". Flag for manual review
    if(fullAddress.find(' OR ') != -1):
        tags.update({'addr:full':fullAddress})
        tags.update({'FIXME':'OR in address. Bailing'})
        return tags
    
    match = re.match('(.*),(.*)', fullAddress)
    if(match):
        tags.update({'FIXME':'apt/ste/lot: ' + match.group(2)})
        fullAddress = match.group(1)
        
    remainingAddress = fullAddress
    streetName = ''
    match = re.match('(\d+) (.*)', fullAddress) #look for house number
    if(match):
        tags.update({'addr:housenumber':match.group(1)})
        remainingAddress = match.group(2)
    else: #address doesn't start with a number. We can't do anything here
        return
    
    #look for directional prefix
    match = re.match('(N|S|E|W{1}) (.*)', remainingAddress) 
    if(match):
        streetName = directionPrefixes[match.group(1)] + ' '
        remainingAddress = match.group(2)

    #parse the rest of the name. Street name and type
    match = re.match('(.*) (.*)', remainingAddress)
    if(match):
        streetName += match.group(1).title() + ' '
        streetName += streetType[match.group(2)]
        tags.update({'addr:street':streetName})
    
    return tags