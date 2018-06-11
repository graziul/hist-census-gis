from histcensusgis.microdata import *
from histcensusgis.Clean import clean_microdata

city_name = sys.argv[0]
state_abbr = sys.argv[1]
decade = sys.argv[2]
ed_map_flag = sys.argv[3]
city_info = [city_name, state_abbr, decade]
clean_microdata(city_info=city_info, ed_map=ed_map_flag)
