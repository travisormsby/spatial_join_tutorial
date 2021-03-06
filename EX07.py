import arcpy
from arcgis.gis import GIS
import pandas as pd

workspace = r'C:\\file\path\to\project.gdb'  #change this filepath
arcpy.env.workspace = workspace

gis = GIS('Pro')

data = gis.content.get('0b028b120b0e41ba833ce47312222c49')

for feature_layer in data.layers:
    sdf = pd.DataFrame.spatial.from_layer(feature_layer)
    sdf.spatial.to_featureclass(location=feature_layer.properties.name)

target_features= 'Address_Points'
join_features= 'Buildings'
out_feature_class='Address_with_building'
join_operation='JOIN_ONE_TO_ONE'
join_type = 'KEEP_ALL'
match_option='CLOSEST'
search_radius='30 Meters'


arcpy.analysis.SpatialJoin(target_features=target_features, 
                           join_features=join_features, 
                           out_feature_class=out_feature_class, 
                           join_operation=join_operation, 
                           join_type=join_type,  
                           match_option=match_option, 
                           search_radius=search_radius)

field_mapping = arcpy.FieldMappings()

name = arcpy.FieldMap()
total_val = arcpy.FieldMap()

name.addInputField('City', 'Name')

total_val.addInputField('Buildings', 'Assessed_Value')
total_val.mergeRule = 'SUM'

name_out = name.outputField
name_out.name = 'Name'
name_out.aliasName = 'Name'
name.outputField = name_out

total_val_out = total_val.outputField
total_val_out.name = 'Total_Prop_Val'
total_val_out.aliasName = 'Total Property Value'
total_val.outputField = total_val_out

field_mapping.addFieldMap(name)
field_mapping.addFieldMap(total_val)

target_features= 'City'
join_features= 'Buildings'
out_feature_class='City_Prop_Val'
join_operation='JOIN_ONE_TO_ONE'
join_type = 'KEEP_ALL'
match_option='CONTAINS'

arcpy.analysis.SpatialJoin(target_features=target_features, 
                           join_features=join_features, 
                           out_feature_class=out_feature_class, 
                           join_operation=join_operation, 
                           join_type=join_type, 
                           field_mapping=field_mapping,
                           match_option=match_option)
