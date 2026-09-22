#Kaeleana Ramirez
#GEOG 676 - Lab 3
#Object-oriented programming with shapes

import math
from pathlib import Path


class Shape:
    def getArea(self):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def getArea(self):
        return self.length * self.width


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def getArea(self):
        return math.pi * self.radius ** 2


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def getArea(self):
        return self.base * self.height / 2


#Create an empty list for the shape objects
shapes = []

#Find shape.txt in the same folder as this Python file
shape_file = Path(__file__).with_name("shape.txt")

#Open and read the supplied data file
with open(shape_file, "r") as file:
    for line in file:
        parts = line.strip().split(",")
        shape_name = parts[0]

        if shape_name == "Rectangle":
            shape = Rectangle(float(parts[1]), float(parts[2]))

        elif shape_name == "Circle":
            shape = Circle(float(parts[1]))

        elif shape_name == "Triangle":
            shape = Triangle(float(parts[1]), float(parts[2]))

        else:
            print("Unknown shape:", shape_name)
            continue

        shapes.append(shape)


#Loop through the objects and print their areas
for shape in shapes:
    print(type(shape).__name__, "area:", shape.getArea())