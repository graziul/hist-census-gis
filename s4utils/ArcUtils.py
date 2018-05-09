import arcpy
import os

# Wrapper function for arcpy.SpatialJoin. By default, returns a reference to a temporary output file in the
# Scratch GDB, with all fields the same as the two parent files, and with JOIN_ONE_TO_MANY.
# By default, only those target features that have the specified match_option with the join features will be kept.
def spatial_join(target,join,match_option, output_fields = 'ALL', output_file = None, join_operation = 'JOIN_ONE_TO_MANY') :
    if not output_file :
        output_file = os.path.join(arcpy.env.scratchGDB,'join_lyr')
    targ_fields = arcpy.ListFields(target)
    join_fields = arcpy.ListFields(join)
    targ_field_names = [x.name for x in targ_fields]
    join_field_names = [x.name for x in join_fields]
    if output_fields == 'ALL' :
        output_fields = targ_fields
        output_fields.extend(join_fields)
    else :
        temp = []
        for field in output_fields :
            #output fields is a user-defined list of field names - convert to field objects from appropriate files
            if field in targ_field_names :
                temp.append([x for x in targ_fields if x.name == field])
            else :
                temp.append([x for x in join_fields if x.name == field])
        output_fields = temp
    field_mapping = ''
    for f in output_fields :
        if f.name in targ_field_names :
            src_file = target
        else :
            src_file = join
        s = '{0} "{1}" {2} {3} {4} {5} {6} {7} {8} ,{9},#,{10},{11},-1,-1;'.format(
            f.name,f.aliasName,f.editable,f.isNullable,f.required,f.length,f.type,
            f.scale,f.precision,"First",src_file,f.name)
        field_mapping += s

    arcpy.SpatialJoin_analysis(target,join,output_file,join_operation,'KEEP_COMMON',field_mapping,match_option)           
    return output_file

""" pblk_id "pblk_id" true true false 10 Long 0 10 ,First,#,%s,pblk_id,-1,-1;
    FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
    grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1"""
"""
Name = POP1990 
Alias = "POP1990" 
Editable = true 
Is Nullable = true 
Required = false 
Length = 4 
Type = Long 
scale = 0
precision = 10
Merge rule = First
joinDelimiter = # (meaning '', null string)
Data source = Database Connections\\dbo@esrigdb.sde\\esrigdb.DBO.cities
Output field name = POP1990
-1
-1
"""
