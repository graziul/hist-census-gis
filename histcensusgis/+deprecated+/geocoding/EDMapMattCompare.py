#Compares ED Maps created using the geocoding method (Matt) vs. the street intersections method (Amory)
#and outputs some statistics (the numbers represent blocks)
print("Importing ArcPy")
import arcpy

verbose = False

for city in ["Atlanta","Akron","Boston","Buffalo","Dayton","Philadelphia","StLouis","SanDiego"] :

    targ = r"S:\Projects\1940Census\%s\GIS_edited\%s_1930_Pblk.shp" % (city,city)
    matt = r"S:\Projects\1940Census\%s\GIS_edited\%s_1930_ED_Choice_Map.shp" % (city,city)

    field_names = [x.name for x in arcpy.ListFields(targ)]
    field_names_matt = [x.name for x in arcpy.ListFields(matt)]


    matt_ed_in_ed_sing = 0
    matt_ed_in_ed_mult = 0
    matt_ed_undefined_amory_mult = 0
    matt_ed_not_in_ed = 0
    ed_undefined = 0
    both_undefined = 0
    matt_ed_undefined_amory_sing = 0
    total_count = 0


    cursor = arcpy.SearchCursor(targ)
    matt_cursor = arcpy.SearchCursor(matt)
    row = cursor.next()
    matt_row = matt_cursor.next()

    print("Running Analysis")

    while row and matt_row :
        total_count +=1
        pblk = int(row.getValue("pblk_id"))
        matt_pblk = int(matt_row.getValue("pblk_id"))
        assert pblk == matt_pblk
        ed = row.getValue("AmoryED")
        ed = [int(x) for x in ed.split('|')]
        matt_ed = int(matt_row.getValue("ed"))

        if matt_ed == 0 and ed == [0] :
            both_undefined += 1
        else :
            if ed == [0] :
                ed_undefined += 1
            elif matt_ed == 0 :
                if len(ed) == 1 :
                    matt_ed_undefined_amory_sing += 1
                else :
                    matt_ed_undefined_amory_mult += 1
            else : #(if ed != 0 and matt_ed != 0)
                if not matt_ed in ed :
                    matt_ed_not_in_ed += 1
                else :
                    if len(ed) == 1:
                        matt_ed_in_ed_sing += 1
                    else :
                        matt_ed_in_ed_mult += 1
        
        
        row = cursor.next()
        matt_row = matt_cursor.next()

    print(city)
    if verbose :
        print("matt_ed_equals_Amory_ed: "+str(matt_ed_in_ed_sing)+" ("+str(round(float(100*matt_ed_in_ed_sing)/float(total_count),1))+"%)")
        print("amory_ed_list_contains_matt_ed: "+str(matt_ed_in_ed_mult)+" ("+str(round(float(100*matt_ed_in_ed_mult)/float(total_count),1))+"%)")
        print("matt_ed_not_in_Amory_ed_list: "+str(matt_ed_not_in_ed)+" ("+str(round(float(100*matt_ed_not_in_ed)/float(total_count),1))+"%)")
        print("just_matt_ed_undefined_amory_single: "+str(matt_ed_undefined_amory_sing)+" ("+str(round(float(100*matt_ed_undefined_amory_sing)/float(total_count),1))+"%)")
        print("just_matt_ed_undefined_amory_multi: "+str(matt_ed_undefined_amory_mult)+" ("+str(round(float(100*matt_ed_undefined_amory_mult)/float(total_count),1))+"%)")
        print("just_amory_ed_undefined: "+str(ed_undefined)+" ("+str(round(float(100*ed_undefined)/float(total_count),1))+"%)")
        print("both_undefined: "+str(both_undefined)+" ("+str(round(float(100*both_undefined)/float(total_count),1))+"%)")
        print("total_blocks: "+str(total_count))
    else :
        print(matt_ed_in_ed_sing)
        print(matt_ed_in_ed_mult)
        print(matt_ed_not_in_ed)
        print(matt_ed_undefined_amory_sing)
        print(matt_ed_undefined_amory_mult)
        print(ed_undefined)
        print(both_undefined)
        print(total_count)
