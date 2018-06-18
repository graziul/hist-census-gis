#!/usr/bin/env python

from histcensusgis.microdata import *
from histcensusgis.Clean import clean_microdata

city_name = sys.argv[1]
state_abbr = sys.argv[2]
decade = sys.argv[3]
ed_map_flag = sys.argv[4]
city_info = [city_name, state_abbr, decade]
print(city_info, ed_map_flag)
clean_microdata(city_info=city_info, ed_map=ed_map_flag)
