import arcpy


working_folder = r"C:\Users\akisch\Desktop\Streetgrid Automation Scripts"
targ = r"C:\Users\akisch\Desktop\Streetgrid Automation Scripts\Cincinnati_OH_1930_EDChiSpaTab.dbf"

#remember the zeros (need to be treated as a special case)

# Version of Dict_append that only accepts unique v(alues) for each k(ey)
def Dict_append_unique(Dict, k, v) :
    if not k in Dict :
        Dict[k] = [v]
    else :
        if not v in Dict[k] :
            Dict[k].append(v)


field_names = [x.name for x in arcpy.ListFields(targ)]
cursor = arcpy.da.SearchCursor(targ, field_names)
silly_dict = {}

for row in cursor :
    Dict_append_unique(silly_dict,row[2],row[3])
    Dict_append_unique(silly_dict,row[2],row[2])


output = working_folder+"\\formattedEDs.dbf"
arcpy.CreateTable_management(working_folder, "formattedEDs.dbf")

arcpy.AddField_management (output, "ed", "SHORT")
arcpy.AddField_management (output, "contig_ed", "TEXT")

rows = arcpy.InsertCursor(output)

for k, v in silly_dict.items() :
    row = rows.newRow()
    row.setValue("ed",k)
    v = [str(x) for x in v]
    row.setValue("contig_ed",";".join(v))
    rows.insertRow(row)

del row
del rows
