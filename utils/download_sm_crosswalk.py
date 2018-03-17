import re
import urllib



state_list = ["ri"]


# Dict: add v(alue) to k(ey), create k if it doesn't exist
def Dict_append(Dict, k, v) :
    if not k in Dict :
        Dict[k] = [v]
    else :
        Dict[k].append(v)

# Version of Dict_append that only accepts unique v(alues) for each k(ey)
def Dict_append_unique(Dict, k, v) :
    if not k in Dict :
        Dict[k] = [v]
    else :
        if not v in Dict[k] :
            Dict[k].append(v)

def download_year(year) : #year = 1920 or year = 1940
    for state_abbr in state_list :
        url = "http://stevemorse.org/census/%s/%s.txt" % (str(year),state_abbr) 
        url_handle = urllib.urlopen(url)
        sourcetext = url_handle.readlines()
        url_handle.close()

        if year == 1940 :
            old_year = 1930
        if year == 1920 :
            year = 1930
            old_year = 1920
        year, old_year = str(year),str(old_year)
        county, old_county = '',''
        city = ''
        ed, old_ed = '',''
        county_name,old_county_name = '',''
        for line in sourcetext :
            line = line.strip()
            if line[:2] == '**' or line == '' :
                continue
            if line[0] == '+' : #line defining a county number
                year_county = re.search("\+([0-9]+)=([0-9%]+),(.*)",line)
                line_year,line_county,line_county_name = year_county.group(1),year_county.group(2),year_county.group(3)
                if line_year == year :
                    if line_county == '%' : #"%" sign means number is same as old number
                        county = old_county
                    else :
                        county = line_county
                    if line_county_name == '%' :
                        county_name = old_county_name
                    else :
                        county_name = line_county_name
                if line_year == old_year :
                    old_county = line_county
                    old_county_name = line_county_name
                county_name_county_dict[county_name] = county
                Dict_append_unique(state_county_dict,state_abbr,county)
                if old_county != county or old_county_name != county_name:
                    county_name_county_dict[old_county_name] = old_county
                    county_change_dict[old_county_name] = county_name
                continue
            if line[0] == '^' : #cache value(s) for old_ed
                cache_ed = re.search("\^\*(.+)",line)
                old_ed = cache_ed.group(1)
                continue
            eds_city = re.search("([^*]+)\*([^*]+)\*?(.*)",line)
            ed,line_old_ed,line_city = eds_city.group(1),eds_city.group(2),eds_city.group(3)
            if line_old_ed != '^' :
                old_ed = line_old_ed
            if line_city != "" :
                city = line_city
            if line_city == "#" : # "#" clears previous value for city
                city = ""
            
            Dict_append_unique(ed_old_ed_dict,county+'-'+ed,old_county+'-'+old_ed)
            if city!= "" :
                Dict_append_unique(city_ed_dict,city,county+'-'+ed)
            Dict_append_unique(county_ed_dict,county,ed)
            if county != old_county:
                Dict_append_unique(county_ed_dict,old_county,old_ed)
            
            
            
ed_old_ed_dict = {} #lookup "[county]-[ed]" -> list of old ed(s) corresponding
city_ed_dict = {} #lookup city+state_abbr -> list of eds in city
county_ed_dict = {} #lookup county number -> list of eds in county
state_county_dict = {} #lookup state_abbr -> list of counties in state
county_name_county_dict = {} #lookup county name+state_abbr -> county number
county_change_dict = {} #lookup old_county_name -> county_name
download_year(1940)
