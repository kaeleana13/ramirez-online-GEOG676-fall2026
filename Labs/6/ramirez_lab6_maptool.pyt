#Kaeleana Ramirez
#GEOG 676 - Lab 6
#Map generation toolbox

import arcpy
import os


class Toolbox:
    def __init__(self):
        self.label = "Lab 6 Map Tools"
        self.alias = "lab6maptools"
        self.tools = [GraduatedColorMap]


class GraduatedColorMap:
    def __init__(self):
        self.label = "Create Graduated Color Map"
        self.description = "Creates a graduated color map."
        self.canRunInBackground = False

    def getParameterInfo(self):
        #Original ArcGIS Pro project
        project = arcpy.Parameter(
            displayName="Original ArcGIS Pro Project",
            name="original_project",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        project.filter.list = ["aprx"]

        #Layer to classify
        layer = arcpy.Parameter(
            displayName="Layer to Classify",
            name="input_layer",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )

        #Output folder
        output_folder = arcpy.Parameter(
            displayName="Output Folder",
            name="output_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        #Output project name
        output_name = arcpy.Parameter(
            displayName="Output Project Name",
            name="output_project_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        output_name.value = "Ramirez_Lab6_Output"

        return [project, layer, output_folder, output_name]

    def execute(self, parameters, messages):
        project_path = parameters[0].valueAsText
        selected_layer = parameters[1].valueAsText
        output_folder = parameters[2].valueAsText
        output_name = parameters[3].valueAsText

        if not output_name.lower().endswith(".aprx"):
            output_name = output_name + ".aprx"

        output_project = os.path.join(output_folder, output_name)

        #Start the progressor
        arcpy.SetProgressor(
            "step",
            "Starting Lab 6...",
            0,
            4,
            1
        )

        #Open the project
        arcpy.SetProgressorLabel("Opening the project...")
        project = arcpy.mp.ArcGISProject(project_path)
        arcpy.SetProgressorPosition()

        #Find the selected layer
        arcpy.SetProgressorLabel("Finding the layer...")
        map_layer = None

        for map_item in project.listMaps():
            for layer_item in map_item.listLayers():
                if layer_item.name == selected_layer:
                    map_layer = layer_item
                    break

            if map_layer is not None:
                break

        if map_layer is None:
            raise ValueError("The selected layer was not found.")

        arcpy.SetProgressorPosition()

        #Create the graduated color map
        arcpy.SetProgressorLabel("Creating the graduated color map...")
        symbology = map_layer.symbology
        symbology.updateRenderer("GraduatedColorsRenderer")
        symbology.renderer.classificationField = "Shape_Area"
        symbology.renderer.breakCount = 5

        color_ramps = project.listColorRamps("Oranges (5 Classes)")

        if len(color_ramps) > 0:
            symbology.renderer.colorRamp = color_ramps[0]

        map_layer.symbology = symbology
        arcpy.SetProgressorPosition()

        #Save a copy of the project
        arcpy.SetProgressorLabel("Saving the completed project...")
        project.saveACopy(output_project)
        arcpy.SetProgressorPosition()

        arcpy.AddMessage("Lab 6 completed successfully.")
        arcpy.AddMessage("Saved project: " + output_project)

        arcpy.ResetProgressor()

        return