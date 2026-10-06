# Kaeleana Ramirez
# GEOG 676 - Lab 5
# Creating a toolbox in ArcGIS Pro

import arcpy
import os


class Toolbox(object):

    def __init__(self):
        # Name of my toolbox
        self.label = "Ramirez Lab 5 Toolbox"
        self.alias = "RamirezLab5"

        # Tools inside my toolbox
        self.tools = [GarageTool]


class GarageTool(object):

    def __init__(self):
        # Information about my tool
        self.label = "Garage Building Proximity"
        self.description = "Finds buildings near the TAMU parking garages"
        self.canRunInBackground = False
        self.category = "Building Tools"


    def getParameterInfo(self):
        # Folder where the new geodatabase will be created
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        # Name of the new geodatabase
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        # CSV file containing the garage coordinates
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        # Name for the garage point layer
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        # Original campus geodatabase
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="CampusGDB",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )

        # Distance used to buffer the garages
        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="BufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )

        params = [param0, param1, param2, param3, param4, param5]

        return params


    def isLicensed(self):
        return True


    def updateParameters(self, parameters):
        return


    def updateMessages(self, parameters):
        return


    def execute(self, parameters, messages):
        # Allow old output files to be replaced
        arcpy.AddMessage("Starting my Lab 5 code")
        arcpy.env.overwriteOutput = True

        # Get the folder and geodatabase name from the user
        folder_path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText
        gdb_path = os.path.join(folder_path, gdb_name)

        # Create the new geodatabase
        arcpy.management.CreateFileGDB(folder_path, gdb_name)

        # Get the garage CSV and layer name
        csv_path = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText

        # Turn the CSV coordinates into garage points
        garages = arcpy.management.MakeXYEventLayer(
            csv_path,
            "X",
            "Y",
            garage_layer_name
        )

        garage_points = os.path.join(gdb_path, garage_layer_name)
        arcpy.management.CopyFeatures(garages, garage_points)

        # Copy the campus buildings into the new geodatabase
        campus = parameters[4].valueAsText
        campus_buildings = os.path.join(campus, "Structures")
        buildings = os.path.join(gdb_path, "Buildings")

        arcpy.management.CopyFeatures(campus_buildings, buildings)

        # Project the garage points to match the buildings
        spatial_reference = arcpy.Describe(buildings).spatialReference
        projected_garages = os.path.join(
            gdb_path,
            "Garage_Points_reprojected"
        )

        arcpy.management.Project(
            garage_points,
            projected_garages,
            spatial_reference
        )

        # Buffer the garage points
        buffer_distance = parameters[5].value
        buffered_garages = os.path.join(
            gdb_path,
            "Garage_Points_buffered"
        )

        arcpy.analysis.Buffer(
            projected_garages,
            buffered_garages,
            buffer_distance
        )

        # Find the buildings that intersect the garage buffers
        intersection = os.path.join(
            gdb_path,
            "Garage_Buildings_Intersection"
        )

        arcpy.analysis.Intersect(
            [buffered_garages, buildings],
            intersection,
            "ALL"
        )

        # Export the intersecting buildings to a CSV file
        output_csv = os.path.join(
            folder_path,
            "ramirez_nearby_buildings.csv"
        )

        arcpy.conversion.ExportTable(
            intersection,
            output_csv
        )

        return