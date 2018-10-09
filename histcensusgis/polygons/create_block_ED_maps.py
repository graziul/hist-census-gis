from histcensusgis.polygons.block import *
from histcensusgis.polygons.ed import *
import pandas as pd
import os

file_path='S:/Projects/1940Census'
city_info_file = file_path + '/CityExtractionList.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_df = city_info_df[city_info_df['Status']>0]
city_info_df.loc[:,'city_name'], city_info_df.loc[:,'state_abbr'] = zip(*city_info_df['City'].str.split(','))
city_info_df = city_info_df[['city_name','state_abbr']]
city_info_df['city_name'] = city_info_df['city_name'].str.replace('Saint','St').str.replace(' ','') #have to keep "St. ____"
city_info_df['state_abbr'] = city_info_df['state_abbr'].str.replace(' ','')
city_state_iterator = zip(city_info_df['city_name'],city_info_df['state_abbr'])

def get_4prong_ed_maps() :
        for city, state_abbr in [("Manhattan","NY")] :
                city_info = [city,state_abbr,1930]
                decade = 1930
                geo_path = file_path+'/'+city+'/GIS_edited/'
                paths = "C:/Program Files/R/R-3.5.1/bin/Rscript", file_path+'/'+city
                if not os.path.isdir(geo_path) :
                        geo_path = file_path+'/'+city+state_abbr+'/GIS_edited/'
                        paths = "C:/Program Files/R/R-3.5.1/bin/Rscript", file_path+'/'+city+state_abbr
                if os.path.isdir(geo_path) :
                        os.chdir(geo_path)
                        if not os.path.isfile(city+'_1930_block_guess.shp') :
                                try :
                                        print "Trying to create block guess map for "+city
                                        identify_blocks_geocode(city_info, paths)
                                        identify_blocks_microdata(city_info, paths)
                                
                                except Exception as e:
                                        print city+" failed on block guess algo because "+str(e)
                                        continue
                        if not os.path.isfile(geo_path + city + '_' + str(decade) + '_ed_inter.shp') :
                                try :
                                        print "Trying to create inter ED map for "+city
                                        ed_inter_algo(city_info, paths, "FULLNAME")
                                except Exception as e:
                                        print city+" failed on ed_inter_algo because "+str(e)
                                        continue
                        if not os.path.isfile(geo_path + city + '_' + str(decade) + '_ed_geo.shp') :
                                try :
                                        print "Trying to create geocode ED map for "+city
                                        ed_geocode_algo(city_info, paths)
                                except Exception as e:
                                        print city+" failed on ed_geocode_algo because "+str(e)
                                        continue
                        if not os.path.isfile(geo_path + city + state_abbr + '_' + str(decade) + '_ed_desc.shp') :
                                try :
                                        print "Trying to create desc ED map for "+city
                                        if city == "Birmingham" :
                                                ed_desc_algo(city_info, paths, grid_street_var='FULLNAME',wildcard="Ensley")
                                        else :
                                                ed_desc_algo(city_info, paths)
                                except Exception as e:
                                        print city+" failed on ed_desc_algo because "+str(e)
                                        continue
                        if os.path.isfile(city+'_1930_block_guess.shp') and os.path.isfile(geo_path + city + '_' + str(decade) + '_ed_inter.shp') and os.path.isfile(geo_path + city + '_' + str(decade) + '_ed_geo.shp') and os.path.isfile(geo_path + city + state_abbr + '_' + str(decade) + '_ed_desc.shp') :
                                if not os.path.isfile(geo_path+city + state_abbr+'_1930_ed_guess.shp') :
                                        print "Trying to combine ED maps for "+city
                                        combine_ed_maps(city_info, geo_path, hn_ranges=['LTOADD','LFROMADD','RTOADD','RFROMADD'])
                                        print "Successfully created ED guess map for "+city
                                else :
                                        print "ED guess map already exists for "+city
                                #except Exception as e:
                                 #       print city+" failed on combine_ed_maps because "+str(e)

def check_for_ed_maps() :
        for city, state_abbr in city_state_iterator :
                city_info = [city,state_abbr,1930]
                decade = 1930
                geo_path = file_path+'/'+city+'/GIS_edited/'
                if os.path.isdir(geo_path) :
                        if os.path.isfile(geo_path+city+state_abbr+"_1930_ed_guess.shp") :
                                print "ED Guess Map exists for "+city+state_abbr
