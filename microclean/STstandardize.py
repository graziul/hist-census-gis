#
#   Function to clean street direction and street type
#
#   Author: Amory Kisch
#   Date:   7/17/16
#

import re

def standardize_street(st):
    runAgain = False
    st = st.rstrip('\n')
    orig_st = st

    ###Remove Punctuation, extraneous words at end of stname###
    st = re.sub(r'[\.,]','',st)
    st = re.sub('\\\\','',st)
    st = re.sub(r' \(?([Cc][Oo][Nn][\'Tt]*d?|[Cc][Oo][Nn][Tt][Ii][Nn][Uu][Ee][Dd])\)?$','',st)
    #consider extended a diff stname#
    #st = re.sub(r' [Ee][XxsS][tdDT]+[^ ]*$','',st)

    #Check if st is empty or blank and return empty to [st,DIR,NAME,TYPE]
    if st == '' or st == ' ':
        return ['','','','']
    
    ###stname part analysis###
    DIR = ''
    NAME = ''
    TYPE = ''
 
    # Combinations of directions (has to be run first)
    if re.search(r' ([Nn][\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)$',st):
        st = "NE "+re.sub(r' ([Nn][\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth[\s]+?[Ee]ast)$','',st)
        DIR = 'NE'
    if re.search(r' ([Nn][\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)$',st):
        st = "NW "+re.sub(r' ([Nn][\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)$','',st)
        DIR = 'NW'
    if re.search(r' ([Ss][\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)$',st):
        st = "SE "+re.sub(r' ([Ss][\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)$','',st)
        DIR = 'SE'
    if re.search(r' ([Ss][\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)$',st):
        st = "SW "+re.sub(r' ([Ss][\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)$','',st)
        DIR = 'SW'
   
    #First check if DIR is at end of stname. make sure that it's the DIR and not actually the NAME (e.g. "North Ave" or "Avenue E")#
    if re.search(r' (N|No|No|[Nn][Oo][Rr][Tt][Hh])$',st) and not re.match('^[Nn][Oo][Rr][Tt][Hh]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+N$',st) :
        st = "N "+re.sub(r' (N|No|[Nn][Oo][Rr][Tt][Hh])$','',st)
        DIR = 'N'
    if re.search(r' (S|So|So|[Ss][Oo][Uu][Tt][Hh])$',st) and not re.search('^[Ss][Oo][Uu][Tt][Hh]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+S$',st) :
        st = "S "+re.sub(r' (S|So|[Ss][Oo][Uu][Tt][Hh])$','',st)
        DIR = 'S'
    if re.search(r' ([Ww][Ee][Ss][Tt]|W)$',st) and not re.search('^[Ww][Ee][Ss][Tt]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+W$',st) :
        st = "W "+re.sub(r' ([Ww][Ee][Ss][Tt]|W)$','',st)
        DIR = 'W'
    if re.search(r' ([Ee][Aa][Ss][Tt]|E)$',st) and not re.search('^[Ee][Aa][Ss][Tt]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+E$',st) :
        st = "E "+re.sub(r' ([Ee][Aa][Ss][Tt]|E)$','',st)
        DIR = 'E'

    #See if a st TYPE can be identified#
    st = re.sub(r'[ \-]+([Ss][Tt][Rr]?[Ee]?[Ee]?[Tt]?[SsEe]?|[Ss][\.][Tt]|[Ss][Tt]?.?[Rr][Ee][Ee][Tt])$',' St',st)
    st = re.sub(r'[ \-]+([Aa][Vv]|[Aa][VvBb][Ee][Nn][Uu]?[EesS]?|Aveenue|Avn[e]?ue|[Aa][Vv][Ee])$',' Ave',st)
    st = re.sub(r'[ \-]+([Bb]\'?[Ll][Vv]\'?[Dd]|Bl\'?v\'?d|Blv|Blvi|Bly|Bldv|Bvld|Bol\'d|[Bb][Oo][Uu][Ll][EeAa]?[Vv]?[Aa]?[Rr]?[Dd]?)$',' Blvd',st)
    st = re.sub(r'[ \-]+([Rr][Dd]|[Rr][Oo][Aa][Dd])$',' Road',st)
    st = re.sub(r'[ \-]+[Dd][Rr][Ii]?[Vv]?[Ee]?$',' Drive',st)
    st = re.sub(r'[ \-]+([Cc][Oo][Uu]?[Rr][Tt]|[Cc][Tt])$',' Ct',st)
    st = re.sub(r'[ \-]+([Pp][Ll][Aa]?[Cc]?[Ee]?)$',' Pl',st)
    st = re.sub(r'[ \-]+([Ss][Qq][Uu]?[Aa]?[Rr]?[Ee]?)$',' Sq',st)
    st = re.sub(r'[ \-]+[Cc]ircle$',' Cir',st)
    st = re.sub(r'[ \-]+([Pp]rkway|[Pp]arkway|[Pp]ark [Ww]ay|[Pp]kway|[Pp]ky|[Pp]arkwy|[Pp]rakway|[Pp]rkwy|[Pp]wy)$',' Pkwy',st)
    st = re.sub(r'[ \-]+[Ww][Aa][Yy]$',' Way',st)
    st = re.sub(r'[ \-]+[Aa][Ll][Ll]?[Ee]?[Yy]?$',' Aly',st)
    st = re.sub(r'[ \-]+[Tt][Ee][Rr]+[EeAa]?[Cc]?[Ee]?$',' Ter',st)
    st = re.sub(r'[ \-]+([Ll][Aa][Nn][Ee]|[Ll][Nn])$',' Ln',st)
    st = re.sub(r'[ \-]+([Pp]lzaz|[Pp][Ll][Aa][Zz][Aa])$',' Plaza',st)

    # "Park" is not considered a valid TYPE because it should probably actually be part of NAME #
    match = re.search(r' (St|Ave|Blvd|Pl|Drive|Road|Ct|Railway|CityLimits|Hwy|Fwy|Pkwy|Cir|Ter|Ln|Way|Trail|Sq|Aly|Bridge|Bridgeway|Walk|Crescent|Creek|River|Line|Plaza|Esplanade|[Cc]emetery|Viaduct|Trafficway|Trfy|Turnpike)$',st)
    if match :
        TYPE = match.group(1)

    #Combinations of directions (assumes no streets named "Northeast Ave" or similar)
    if re.search(r'^([Nn][\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)[ \-]+',st):
        st = "NE "+re.sub(r'^([Nn][\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)[ \-]+','',st)
        DIR = 'NE'
    if re.search(r'^([Nn][\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)[ \-]+',st):
        st = "NW "+re.sub(r' ([Nn][\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)[ \-]+','',st)
        DIR = 'NW'
    if re.search(r'^([Ss][\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)[ \-]+',st):
        st = "SE "+re.sub(r'^([Ss][\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)[ \-]+','',st)
        DIR = 'SE'
    if re.search(r'^([Ss][\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)[ \-]+',st):
        st = "SW "+re.sub(r'^([Ss][\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)[ \-]+','',st)
        DIR = 'SW'
        
    #See if there is a st DIR. again, make sure that it's the DIR and not actually the NAME (e.g. North Ave)
    match =  re.search(r'^([nN]|N\.|No|No\.|[Nn][Oo][Rr][Tt]?[Hh]?)[ \-]+',st)
    if match :
        if st==match.group(0)+TYPE:
            NAME = 'North'
        else :
            st = "N "+re.sub(r'^([nN]|N\.|No|No\.|[Nn][Oo][Rr][Tt]?[Hh]?)[ \-]+','',st)
            DIR = 'N'
    match =  re.search(r'^([sS]|S\.|So|So\.|[Ss][Oo][Uu][Tt]?[Hh]?)[ \-]+',st)
    if match :
        if st==match.group(0)+TYPE:
            NAME = 'South'
        else :
            st = "S "+re.sub(r'^([sS]|S\.|So|So\.|[Ss][Oo][Uu][Tt]?[Hh]?)[ \-]+','',st)
            DIR = 'S'
    match =  re.search(r'^([wW]|[Ww]\.|[Ww][Ee][Ss]?[Tt]?[\.]?)[ \-]+',st)
    if match :
        if st==match.group(0)+TYPE:
            NAME = 'West'
        else :
            st = "W "+re.sub(r'^([wW]|[Ww]\.|[Ww][Ee][Ss]?[Tt]?[\.]?)[ \-]+','',st)
            DIR = 'W'
    match =  re.search(r'^([eE]|[Ee][\.\,]|[Ee][Ee]?[Aa]?[Ss][Tt][\.]?|Ea[Ss]?)[ \-]+',st)
    if match :
        if st==match.group(0)+TYPE:
            NAME = 'East'
        else :
            st = "E "+re.sub(r'^([eE]|[Ee][\.\,]|[Ee][Ee]?[Aa]?[Ss][Tt][\.]?|Ea[Ss]?)[ \-]+','',st)
            DIR = 'E'
    
    #get the st NAME and standardize it
    #convert written-out numbers to digits
    #TODO: Make these work for all exceptions (go thru text file with find)
    if re.search("[Tt]enth|Eleven(th)?|[Tt]wel[f]?th|[Tt]hirteen(th)?|Fourt[h]?een(th)?|[Ff]ift[h]?een(th)?|[Ss]event[h]?een(th)?|[Ss]event[h]?een(th)?|[eE]ighteen(th)?|[Nn]inet[h]?een(th)?|[Tt]wentieth|[Tt]hirtieth|[Ff]o[u]?rtieth|[Ff]iftieth|[Ss]ixtieth|[Ss]eventieth|[Ee]ightieth|[Nn]inetieth|Twenty[ \-]?|Thirty[ \-]?|Forty[ \-]?|Fifty[ \-]?|Sixty[ \-]?|Seventy[ \-]?|Eighty[ \-]?|Ninety[ \-]?|[Ff]irst|[Ss]econd|[Tt]hird|[Ff]ourth|[Ff]ifth|[Ss]ixth|[Ss]eventh|[Ee]ighth|[Nn]inth",st) :
        st = re.sub("[Tt]enth","10th",st)
        st = re.sub("[Ee]leven(th)?","11th",st)
        st = re.sub("[Tt]wel[f]?th","12th",st)
        st = re.sub("[Tt]hirteen(th)?","13th",st)
        st = re.sub("[Ff]ourt[h]?een(th)?","14th",st)
        st = re.sub("[Ff]ift[h]?een(th)?","15th",st)
        st = re.sub("[Ss]ixt[h]?een(th)?","16th",st)
        st = re.sub("[Ss]event[h]?een(th)?","17th",st)
        st = re.sub("[eE]ighteen(th)?","18th",st)
        st = re.sub("[Nn]inet[h]?een(th)?","19th",st)
        st = re.sub("[Tt]wentieth","20th",st)
        st = re.sub("[Tt]hirtieth","30th",st)
        st = re.sub("[Ff]o[u]?rtieth","40th",st)
        st = re.sub("[Ff]iftieth", "50th",st)
        st = re.sub("[Ss]ixtieth", "60th",st)
        st = re.sub("[Ss]eventieth", "70th",st)
        st = re.sub("[Ee]ightieth", "80th",st)
        st = re.sub("[Nn]inetieth", "90th",st)

        st = re.sub("Twenty[ \-]?","2",st)
        st = re.sub("Thirty[ \-]?","3",st)
        st = re.sub("Forty[ \-]?","4",st)
        st = re.sub("Fifty[ \-]?","5",st)
        st = re.sub("Sixty[ \-]?","6",st)
        st = re.sub("Seventy[ \-]?","7",st)
        st = re.sub("Eighty[ \-]?","8",st)
        st = re.sub("Ninety[ \-]?","9",st)
        st = re.sub("[Ff]irst","1st",st)
        st = re.sub("[Ss]econd","2nd",st)
        st = re.sub("[Tt]hird","3rd",st)
        st = re.sub("[Ff]our(th)?","4th",st)
        st = re.sub("[Ff]ifth","5th",st)
        st = re.sub("[Ss]ix(th)?","6th",st)
        st = re.sub("[Ss]even(th)?","7th",st)
        st = re.sub("[Ee]ighth?","8th",st)
        st = re.sub("[Nn]in(th|e)","9th",st)
        
    match = re.search(DIR+'(.+)'+TYPE,st)
    if NAME=='' :
        #If NAME is not 'North', 'West', etc...
        if match :
            NAME = match.group(1).strip()
            if re.search("[0-9]+",NAME) :
                # TODO: Fix incorrect suffixes e.g. "73d St"
                '''
                if re.search("^[0-9]+[Ss][Tt]",NAME):
                    NAME = re.sub("[Ss][Tt]","st",NAME)
                if re.search("^[0-9]+[Rr][Dd]",NAME):
                    NAME = re.sub("[Rr][Dd]","rd",NAME)
                if re.search("^[0-9]+[Nn][Dd]",NAME):
                    NAME = re.sub("[Nn][Dd]","nd",NAME)
                if re.search("^[0-9]+[Tt][Hh]",NAME):
                    NAME = re.sub("[Tt][Hh]","th",NAME)     
                '''             
                # TODO: identify corner cases with numbers e.g. "51 and S- Hermit"
                if re.search("^[0-9]+$",NAME) : #if NAME is only numbers (no suffix)
                    foo = True
                    suffixes = {'11':'11th','1':'1st','2':'2nd','3':'3rd','4':'4th','5':'5th','6':'6th','7':'7th','8':'8th','9':'9th','0':'0th'}
                    num = re.search("[0-9]$",NAME)
                    NAME = re.sub("[0-9]$",suffixes[num.group(0)],NAME)
                hnum = re.search("^([0-9]+[ \-]+).+",NAME) #housenum in stname?
                if hnum : 
                    NAME = re.sub(hnum.group(1),"",NAME) #remove housenum. May want to update housenum field, maybe not though.
                    runAgain = True
            else :
                NAME = NAME.title()
            
        else :
            assert(False)
        # Standardize "Saint ____ Ave" -> "St ____ Ave" #
        NAME = re.sub("^([Ss][Tt]\.?|[Ss][Aa][Ii][Nn][Tt])[ \-]","St ",NAME)
    st = re.sub(re.escape(match.group(1).strip()),NAME,st).strip()
    try :
        assert st == (DIR+' '+NAME+' '+TYPE).strip()
    except AssertionError :
        print("Something went horribly wrong while trying to pre-standardize stnames.")
        print("orig was: "+orig_st)
        print("st is: \""+st+"\"")
        print("components: \""+(DIR+' '+NAME+' '+TYPE).strip()+"\"")
    
    if runAgain :
        return standardize_street(st)
    else :
        return [st, DIR, NAME, TYPE]

