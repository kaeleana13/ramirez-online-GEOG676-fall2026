#Kaeleana Ramirez
#GEOG 676 - Lab 7
#Raster analysis

import arcpy
from pathlib import Path


#Find the folders containing the files
folder = Path(__file__).parent
landsat_folder = folder / "landsat4"
dem_folder = folder / "dem"

#Assign the four Landsat bands
band1 = arcpy.sa.Raster(str(landsat_folder / "blue.tif"))
band2 = arcpy.sa.Raster(str(landsat_folder / "green.tif"))
band3 = arcpy.sa.Raster(str(landsat_folder / "red.tif"))
band4 = arcpy.sa.Raster(str(landsat_folder / "nir08.tif"))

#Create the composite raster
composite_output = folder / "ramirez_composite.tif"

arcpy.management.CompositeBands(
    [band1, band2, band3, band4],
    str(composite_output)
)

print("Composite raster created")

#Create the hillshade raster
dem = dem_folder / "dem_30m.tif"
hillshade_output = folder / "ramirez_hillshade.tif"

arcpy.ddd.HillShade(
    str(dem),
    str(hillshade_output),
    315,
    45,
    "NO_SHADOWS",
    1
)

print("Hillshade raster created")

#Create the slope raster
slope_output = folder / "ramirez_slope.tif"

arcpy.ddd.Slope(
    str(dem),
    str(slope_output),
    "DEGREE",
    1
)

print("Slope raster created")
print("Lab 7 completed successfully")