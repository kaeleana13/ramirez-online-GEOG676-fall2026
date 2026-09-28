# GEOG 676 Lab 4: Fun with ArcPy

This lab uses ArcPy to create garage points from a CSV file, create a
file geodatabase, buffer the garage points, intersect the buffers with
campus buildings, and export the results to a CSV file.

I used a buffer distance of 150 meters. The intersection produced 62
building records.

## Files

- `ramirez_lab4_arcpy.py` - Python code
- `Ramirez_Lab4.gdb.zip` - Output geodatabase
- `ramirez_nearby_buildings.csv` - Intersection results
- `ramirez_lab4_results.png` - Screenshot of the executed code
