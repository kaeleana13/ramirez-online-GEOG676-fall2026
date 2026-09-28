#Kaeleana Ramirez
#GEOG 676 - Lab 4
#Fun with ArcPy

import arcpy
from pathlib import Path


#Find the Lab 4 files
lab_folder = Path(__file__).resolve().parent
garage_csv = lab_folder / "garages.csv"
campus_gdb = lab_folder / "Campus.gdb"

#Name my outputs
output_gdb = lab_folder / "Ramirez_Lab4.gdb"
output_csv = lab_folder / "ramirez_nearby_buildings.csv"


#Make sure the input files are available
if not garage_csv.exists():
    raise FileNotFoundError("garages.csv was not found")

if not campus_gdb.exists():
    raise FileNotFoundError("Campus.gdb was not found")


arcpy.env.overwriteOutput = True

print("Starting Lab 4...")


#Create my geodatabase
if arcpy.Exists(str(output_gdb)):
    arcpy.management.Delete(str(output_gdb))

arcpy.management.CreateFileGDB(
    str(lab_folder),
    output_gdb.name
)

print("Created Ramirez_Lab4.gdb")


#Create garage points from the CSV
garage_layer = "garage_xy_layer"
garage_points = output_gdb / "Garage_Points_WGS84"
wgs84 = arcpy.SpatialReference(4326)

arcpy.management.MakeXYEventLayer(
    str(garage_csv),
    "X",
    "Y",
    garage_layer,
    wgs84
)

arcpy.management.CopyFeatures(
    garage_layer,
    str(garage_points)
)

print("Created the garage points")


#Copy the campus buildings into my geodatabase
campus_structures = campus_gdb / "Structures"
buildings = output_gdb / "Structures"

if not arcpy.Exists(str(campus_structures)):
    raise FileNotFoundError(
        "Structures was not found in Campus.gdb"
    )

arcpy.management.CopyFeatures(
    str(campus_structures),
    str(buildings)
)

print("Copied the Structures layer")


#Project the garage points to match the buildings
building_projection = arcpy.Describe(
    str(buildings)
).spatialReference

projected_garages = output_gdb / "Garage_Points_Projected"

arcpy.management.Project(
    str(garage_points),
    str(projected_garages),
    building_projection
)

print("Projected the garage points")


#Ask the user for the buffer distance
while True:
    try:
        buffer_distance = float(
            input("Enter buffer distance in meters: ")
        )

        if buffer_distance > 0:
            break

        print("Enter a number greater than zero")

    except ValueError:
        print("Enter a valid number")


#Buffer the garage points
garage_buffers = output_gdb / "Garage_Points_Buffered"

arcpy.analysis.Buffer(
    str(projected_garages),
    str(garage_buffers),
    f"{buffer_distance} Meters"
)

print("Buffered the garage points")


#Intersect the buffers with the buildings
intersection = output_gdb / "Garage_Building_Intersection"

arcpy.analysis.Intersect(
    [str(garage_buffers), str(buildings)],
    str(intersection),
    "ALL"
)

print("Intersected the garage buffers and buildings")


#Export the results to a CSV
if output_csv.exists():
    output_csv.unlink()

arcpy.conversion.ExportTable(
    str(intersection),
    str(output_csv)
)


#Print the final results
result_count = int(
    arcpy.management.GetCount(str(intersection))[0]
)

print("--------------------------------")
print("Lab 4 completed successfully")
print("Buffer distance:", buffer_distance, "meters")
print("Intersecting building records:", result_count)
print("CSV created:", output_csv.name)