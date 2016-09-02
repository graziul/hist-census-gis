import urllib
import pandas as pd
import re
import pickle

# Use one year's CityInfo file to get list of states
file_path = '/home/s4-data/LatestCities' 
city_info_file = file_path + '/CityInfo.csv' 
city_info_df = pd.read_csv(city_info_file)

state_list = city_info_df['state_abbr'].str.lower().unique().tolist()
city_list = city_info_df['city_name'].tolist()

city_state_iterator = zip(city_info_df['city_name'].tolist(),city_info_df['state_abbr'].str.lower().tolist())

def get_sm_web_abbr(year):

    for city_state in city_state_iterator:

        city_name = city_state[0]
        state_abbr = city_state[1]

        url = "http://www.stevemorse.org/census/%sstates/%s.htm" % (str(year),state_abbr) 

        url_handle = urllib.urlopen(url)
        sourcetext = url_handle.readlines()
        url_handle.close()

        #Change the parsing strings if necessary (CG: Doesn't seem necessary yet)
        start_num = "value=" 
        end_num = ">"
        end_name = "</option>"

        for line in sourcetext:
            #If line has "value=" and "</option>" in it, do stuff
            if start_num in line and end_name in line:
                #Ignore header line
                if "Select City" in line:
                    continue
                if "Other" in line:
                    continue
                else:
                    city = line[line.find(end_num)+1:line.find("(")].rstrip().replace('.','')
                    city_abbr = line[line.find(start_num) + 7 : line.find(end_num)-1].lower()
                    city_abbr = re.sub(r'\$[0-9]','',city_abbr)
                    sm_web_abbr_dict[year][state_abbr][city_name] = city_abbr + state_abbr

sm_web_abbr_dict = {}
for year in [1900,1910,1930,1940]:
    sm_web_abbr_dict[year] = {}
    for state_abbr in state_list:
        sm_web_abbr_dict[year][state_abbr] = {}
    get_sm_web_abbr(year)

pickle.dump(sm_web_abbr_dict,open(file_path + '/sm_web_abbr.pickle','wb'))

def sm_standardize(st) :
    orig_st = st
    st = re.sub(" [Ee][Xx][Tt][Dd]?$","",st)
    DIR = re.search(" ([NSEW]+)$",st)
    st = re.sub(" ([NSEW]+)$","",st)
    if(DIR) :
        DIR = DIR.group(1)
    else :
        DIR = ""

    TYPE = re.search(r' (St|Ave?|Blvd|Pl|Dr|Rd|Ct|Railway|CityLimits|Hwy|Fwy|Pkwy|Cir|Ter|Ln|Way|Trail|Sq|All?e?y?|Bridge|Bridgeway|Walk|Crescent|Creek|River|Line|Plaza|Esplanade|[Cc]emetery|Viaduct|Trafficway|Trfy|Turnpike)$',st)
    
    if(TYPE) :
        st = re.sub(TYPE.group(0),"",st)
        TYPE = TYPE.group(1)
        if(TYPE=="Av") :
            TYPE = "Ave"
        if(TYPE=="Rd") :
            TYPE = "Road"
        if(TYPE=="Dr") :
            TYPE = "Drive"
        if(re.match("All?e?y?",TYPE)) :
            TYPE = "Aly"
    else :
        TYPE = "St"
    
    NAME = st
    st = (DIR+" "+NAME+" "+TYPE).strip()
#    print(orig_st)
#    print("changed to "+st)
    return [st,DIR,NAME,TYPE]

def get_sm_st_ed(year):
        
    for city_state in city_state_iterator:

        city_name = city_state[0]
        state_abbr = city_state[1]
  
        # Some state-years don't have data on Steve Morse website      
        try:
            sm_web_abbr = sm_web_abbr_dict[year][state_abbr][city_name]
        except:
            continue

        url = "http://www.stevemorse.org/census/%scities/%s.htm" % (str(year),sm_web_abbr) 

        url_handle = urllib.urlopen(url)
        sourcetext = url_handle.readlines()
        url_handle.close()

        #Change the parsing strings if necessary (CG: Doesn't seem necessary yet)
        start_num = "value=" 
        end_num = ">"
        end_name = "</option>"

        sm_st_ed_dict_city = {}

        for line in sourcetext:
            #If line has "value=" and "</option>" in it, do stuff
            if start_num in line and end_name in line:
                #Ignore header line
                if "Select Street" in line:
                    col_line = ""
                else:
                    #Extract street name between ">" and "</option>""
                    st = line[line.find(end_num)+1:line.find(end_name)]
                    st = sm_standardize(st)
                    #Initialize dictionary for NAME if it doesn't exist already
                    NAME = st[2]
                    sm_st_ed_dict_city[NAME] = {}
                    #Extract EDs as one long string
                    st_str = line[line.find(start_num) + 7 : line.find(end_num)-1]
                    #Split string of EDs into a list and assign to street name in dictionary
                    sm_st_ed_dict_city[NAME].update({st[0]:list(st_str.split(","))})
        sm_st_ed_dict[year][city_state] = sm_st_ed_dict_city

sm_st_ed_dict ={}
for year in [1900,1910,1930,1940]:
    sm_st_ed_dict[year] = {}
    for city_state in city_state_iterator:
        sm_st_ed_dict[year][city_state] = {}
    get_sm_st_ed(year)

pickle.dump(sm_st_ed_dict,open(file_path + '/sm_st_ed_dict.pickle','wb'))
