#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:46:48 2018

@author: Lukáš Růžička (lruzicka@redhat.com)
"""

import tkinter as tk
from PIL import Image
import os
import json
from tkinter import filedialog, messagebox

class Application:
    """ Hold the GUI frames and widgets, as well as the handling in the GUI. """
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.grid()
        self.buildWidgets()
        self.images = [] # List of images to be handled.
        self.needleCoordinates = [0, 0, 0, 0] # Coordinates of the needle area
        self.directory = "" # Active working directory
        self.rectangle = None # The red frame around the area
        self.needle = needleData({"properties":[], "tags":[], "area":[]}) # The Needle object
        self.imageName = None # The name of the active image
        self.handler = None # The file reader and writer object
        self.imageCount = 0 # Counter for
        
    def buildWidgets(self):
        """Construct GUI"""
        self.buttonFrame = tk.Frame(self.frame)
        self.buttonFrame.grid(row=0, column=0, rowspan=2, sticky="news")

        self.openDirButton = tk.Button(self.buttonFrame, text="Select image directory", width=15, command=self.readimages)
        self.openDirButton.grid(row=0, column=0, sticky="nesw")

        self.quitButton = tk.Button(self.buttonFrame, text="Quit", fg="red", command=self.frame.quit)
        self.quitButton.grid(row=12, column=0, sticky="nesw")
        
        self.nextButton = tk.Button(self.buttonFrame, text="Next image (n)", command=lambda: self.nextImage(None))
        self.nextButton.grid(row=1,  column=0, sticky="nesw")
        
        self.prevButton = tk.Button(self.buttonFrame, text="Previous image (p)", command=lambda: self.prevImage(None))
        self.prevButton.grid(row=2,  column=0, sticky="nesw")
        
        self.createButton = tk.Button(self.buttonFrame, text="Show next area (s)", command=lambda: self.showArea(None))
        self.createButton.grid(row=3,  column=0, sticky="nesw")
        
        self.modifyButton = tk.Button(self.buttonFrame, text="Modify active area (m)", command=lambda: self.modifyArea(None))
        self.modifyButton.grid(row=4, column=0, sticky="nesw")
        
        #self.hideButton = tk.Button(self.buttonFrame, text="Delete active area (d)", command=lambda: self.hideArea(None))
        #self.hideButton.grid(row=5, column=0, sticky="news")
        
        self.addButton = tk.Button(self.buttonFrame, text="Add area to needle (a)", command=lambda: self.addAreaToNeedle(None))
        self.addButton.grid(row=6, column=0, sticky="news")
        
        self.deleteButton = tk.Button(self.buttonFrame, text="Remove area from needle (r)", command=lambda: self.removeAreaFromNeedle(None))
        self.deleteButton.grid(row=7, column=0, sticky="news")
        
        self.loadButton = tk.Button(self.buttonFrame, text="Load needle (l)", command=lambda: self.loadNeedle(None))
        self.loadButton.grid(row=8,  column=0, sticky="nesw")
        
        self.saveButton = tk.Button(self.buttonFrame, text="Create (save) needle (c)", command=lambda: self.createNeedle(None))
        self.saveButton.grid(row=9,  column=0, sticky="nesw")
        
        self.picFrame = tk.Frame(self.frame)
        self.picFrame.grid(row=0, column=1)
                
        self.xscroll = tk.Scrollbar(self.picFrame, orient='horizontal')
        self.xscroll.grid(row=1, column=0, sticky="we")
        
        self.yscroll = tk.Scrollbar(self.picFrame, orient='vertical')
        self.yscroll.grid(row=0, column=1, columnspan=2, sticky="ns")

        self.pictureField = tk.Canvas(self.picFrame, height=800, width=1200, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.pictureField.grid(row=0, column=0)
        self.pictureField.config(scrollregion=self.pictureField.bbox('ALL'))
        self.pictureField.bind("<Button 1>", self.startArea)
        self.pictureField.bind("<B1-Motion>", self.redrawArea)
        self.pictureField.bind("<ButtonRelease-1>", self.endArea)
        self.pictureField.bind("m", self.modifyArea)
        self.pictureField.bind("s", self.showArea)
        self.pictureField.bind("n", self.nextImage)
        self.pictureField.bind("a", self.addAreaToNeedle)
        self.pictureField.bind("r", self.removeAreaFromNeedle)
        self.pictureField.bind("p", self.prevImage)
        self.pictureField.bind("l", self.loadNeedle)
        self.pictureField.bind("c", self.createNeedle)
       # self.pictureField.bind("c", self.saveNeedle)
        #self.pictureField.bind("m", lambda: self.modifyNeedle())
        
        self.xscroll.config(command=self.pictureField.xview)
        self.yscroll.config(command=self.pictureField.yview)
        
        self.jsonFrame = tk.Frame(self.frame)
        self.jsonFrame.grid(row=0, column=2, sticky="news")
        
        self.nameLabel = tk.Label(self.jsonFrame, text="Filename:")
        self.nameLabel.grid(row=0, column=0, sticky="w")
        
        self.nameEntry = tk.Entry(self.jsonFrame)
        self.nameEntry.grid(row=1, column=0, sticky="ew")
        
        self.propLabel = tk.Label(self.jsonFrame, text="Properties:")
        self.propLabel.grid(row=2, column=0, sticky="w")
        
        self.propText = tk.Text(self.jsonFrame, width=50, height=5)
        self.propText.grid(row=3, column=0, sticky="ew")

        self.needleUL = tk.Label(self.jsonFrame, text="Area Coordinates:")
        self.needleUL.grid(row=4, column=0, sticky="w")

        self.coordFrame = tk.Frame(self.jsonFrame)
        self.coordFrame.grid(row=5, column=0, sticky="ew")

        self.axLable = tk.Label(self.coordFrame, text="X1:")
        self.axLable.grid(row=0, column=0, sticky="w")
        
        self.axEntry = tk.Entry(self.coordFrame, width=5)
        self.axEntry.grid(row=0, column=1, sticky="w")

        self.ayLable = tk.Label(self.coordFrame, text="Y1:")
        self.ayLable.grid(row=0, column=2, sticky="w")

        self.ayEntry = tk.Entry(self.coordFrame, width=5)
        self.ayEntry.grid(row=0, column=3, sticky="w")

        self.widthLabel = tk.Label(self.coordFrame, text="Area width:")
        self.widthLabel.grid(row=0, column=4, sticky="w")

        self.widthEntry = tk.Entry(self.coordFrame, width=5)
        self.widthEntry.grid(row=0, column=5, sticky="w")

        self.heigthLabel = tk.Label(self.coordFrame, text="Area heigth:")
        self.heigthLabel.grid(row=1, column=4, sticky="w")

        self.heigthEntry = tk.Entry(self.coordFrame, width=5)
        self.heigthEntry.grid(row=1, column=5, sticky="w")

        self.bxLable = tk.Label(self.coordFrame, text="X2:")
        self.bxLable.grid(row=1, column=0, sticky="w")

        self.bxEntry = tk.Entry(self.coordFrame, width=5)
        self.bxEntry.grid(row=1, column=1, sticky="w")

        self.byLable = tk.Label(self.coordFrame, text="Y2:")
        self.byLable.grid(row=1, column=2, sticky="w")

        self.byEntry = tk.Entry(self.coordFrame, width=5)
        self.byEntry.grid(row=1, column=3, sticky="w")

        self.listLabel = tk.Label(self.jsonFrame, text="Area type:")
        self.listLabel.grid(row=6, column=0, sticky="w")
        
        self.typeList = tk.Spinbox(self.jsonFrame, values=["match","ocr","exclude"])
        self.typeList.grid(row=7, column=0, sticky="ew")
        
        self.textLabel = tk.Label(self.jsonFrame, text="Tags:")
        self.textLabel.grid(row=8, column=0, sticky="w")
        
        self.textField = tk.Text(self.jsonFrame, width=50, height=15)
        self.textField.grid(row=9, column=0, sticky="ew")
        
        self.jsonLabel = tk.Label(self.jsonFrame, text="Json Data:")
        self.jsonLabel.grid(row=10, column=0, sticky="w")
        
        self.textJson = tk.Text(self.jsonFrame, width=50, height=15)
        self.textJson.grid(row=11, column=0, sticky="ew")

        self.needleLable = tk.Label(self.jsonFrame, text="Areas in needle: ")
        self.needleLable.grid(row=12, column=0, sticky="w")

        self.needleEntry = tk.Entry(self.jsonFrame, width=5)
        self.needleEntry.grid(row=13, column=0, sticky="w")
        

    def returnPath(self, image):
        """Create a full path from working directory and image name."""
        return os.path.join(self.directory, image)
    
    def readimages(self):
        """Read png images from the given directory and create a list of their names."""
        self.images = []
        self.directory = filedialog.askdirectory()
        if self.directory:
            for file in os.listdir(self.directory):
                if file.endswith(".png"):
                    self.images.append(file)
        else:
            pass
        if len(self.images) == 1:
            messagebox.showinfo("Found images", "Found 1 image in the selected directory.")
        else:
            messagebox.showinfo("Found images", "Found {} images in the selected directory.".format(len(self.images)))
        self.imageCount = 0
        try:
            self.imageName = self.images[0]
            self.displayImage(self.returnPath(self.imageName))
        except IndexError:
            pass

    def displayImage(self, path):
        """Display image on the canvas."""
        print(path)
        self.picture = Image.open(path)
        #width = self.picture.width
        #height = self.picture.height
        self.picsize = (self.picture.width,self.picture.height)
        self.image = tk.PhotoImage(file=path)
        self.background = self.pictureField.create_image((1, 1), image=self.image, anchor='nw')
        self.nameEntry.config(state="normal")
        self.nameEntry.delete(0, "end")
        self.nameEntry.insert("end", self.imageName)
        self.nameEntry.config(state="readonly")
        self.pictureField.focus_set()
               
    def nextImage(self, arg):
        """Display next image on the list."""
        self.imageCount += 1
        try:
            self.imageName = self.images[self.imageCount]
        except IndexError:
            self.imageName = self.images[0]
            self.imageCount = 0
        self.pictureField.delete(self.rectangle)
        self.rectangle = None
        self.displayImage(self.returnPath(self.imageName))

    def prevImage(self, arg):
        """Display previous image on the list."""
        self.imageCount -= 1
        try:
            self.imageName = self.images[self.imageCount]
        except IndexError:
            self.imageName = self.images[-1]
            self.imageCount = len(self.images)
        self.pictureField.delete(self.rectangle)
        self.rectangle = None
        self.displayImage(self.returnPath(self.imageName))
        
    
    def getCoordinates(self):
        """Read coordinates from the coordinate windows."""
        xpos = int(self.axEntry.get())
        ypos = int(self.ayEntry.get())
        apos = int(self.bxEntry.get())
        bpos = int(self.byEntry.get())

        if not xpos and not apos:
            self.needleCoordinates = [0, 0, 100, 200]
        else:
            self.needleCoordinates = [xpos, ypos, apos, bpos]

    def calculateSize(self, coordinates):
        """Calculate size of the area from its coordinates."""
        width = int(coordinates[2]) - int(coordinates[0])
        heigth = int(coordinates[3]) - int(coordinates[1])
        return [width, heigth]
            
    def showArea(self, arg):
        """Load area and draw a rectangle around it."""
        #self.getCoordinates()
        self.area = self.needle.provideNextArea()
        try:
            self.needleCoordinates = [self.area[0], self.area[1], self.area[2], self.area[3]]
            typ = self.area[4]
            self.rectangle = self.pictureField.create_rectangle(self.needleCoordinates, outline="red", width=2)
            self.displayCoordinates(self.needleCoordinates)
            self.typeList.delete(0, "end")
            self.typeList.insert("end", typ)
        except TypeError:
            pass


    def displayCoordinates(self, coordinates):
        """Disply coordinates in the GUI"""
        self.axEntry.delete(0, "end")
        self.axEntry.insert("end", coordinates[0])
        self.ayEntry.delete(0, "end")
        self.ayEntry.insert("end", coordinates[1])
        self.bxEntry.delete(0, "end")
        self.bxEntry.insert("end", coordinates[2])
        self.byEntry.delete(0, "end")
        self.byEntry.insert("end", coordinates[3])
        size = self.calculateSize(coordinates)
        self.widthEntry.delete(0, "end")
        self.widthEntry.insert("end", size[0])
        self.heigthEntry.delete(0, "end")
        self.heigthEntry.insert("end", size[1])
        
    def modifyArea(self, arg):
        """Update the information for the active needle area, including properties, tags, etc."""
        self.getCoordinates()
        xpos = self.needleCoordinates[0]
        ypos = self.needleCoordinates[1]
        apos = self.needleCoordinates[2]
        bpos = self.needleCoordinates[3]
        typ = self.typeList.get()
        props = self.propText.get("1.0", "end-1c")
        if "\n" in props:
            props = props.split("\n")
        if props == "":
            props = []
        tags = self.textField.get("1.0", "end-1c")
        if "\n" in tags:
            tags = tags.split("\n")
        if tags == "":
            tags = []
        coordinates = [xpos, ypos, apos, bpos, typ]
        self.needle.update(coordinates, tags, props)
        self.textJson.delete("1.0", "end")
        json = self.needle.provideJson()
        self.textJson.insert("end", json)
        self.pictureField.coords(self.rectangle, self.needleCoordinates)
        
    def addAreaToNeedle(self, arg):
        """Add new area to needle. The needle can have more areas."""
        self.needle.addArea()
        self.modifyArea(None)
        areas = self.needle.provideAreaCount()
        self.needleEntry.delete(0, "end")
        self.needleEntry.insert("end", areas)


    def removeAreaFromNeedle(self, arg):
        """Remove the active area from the needle (deletes it)."""
        self.needle.removeArea()
        areas = self.needle.provideAreaCount()
        coordinates = [0, 0, 0, 0]
        self.displayCoordinates(coordinates)
        self.needleEntry.delete(0, "end")
        self.needleEntry.insert("end", areas)
        json = self.needle.provideJson()
        self.textJson.delete("1.0", "end")
        self.textJson.insert("end", json)
        self.pictureField.delete(self.rectangle)
        self.rectangle = None
        self.showArea(None)
        
    def startArea(self, event):
        """Get coordinates on mouse click and start drawing the rectangle from this point."""
        xpos = event.x
        ypos = event.y
        self.startPoint = [xpos, ypos]
        if self.rectangle == None:
            self.rectangle = self.pictureField.create_rectangle(self.needleCoordinates, outline="red", width=2)
            
    def redrawArea(self, event):
        """Upon mouse drag update the size of the rectangle as the mouse is moving."""
        apos = event.x
        bpos = event.y
        self.endPoint = [apos, bpos]
        self.needleCoordinates = self.startPoint + self.endPoint
        self.pictureField.coords(self.rectangle, self.needleCoordinates)
        
    def endArea(self, event):
        """Stop drawing the rectangle and record the coordinates to match the final size."""
        coordinates = [0, 0, 1, 1]
        xpos = self.needleCoordinates[0]
        ypos = self.needleCoordinates[1]
        apos = self.needleCoordinates[2]
        bpos = self.needleCoordinates[3]
        self.pictureField.focus_set()
        
        if xpos <= apos and ypos <= bpos:
            coordinates[0] = xpos
            coordinates[1] = ypos
            coordinates[2] = apos
            coordinates[3] = bpos
        elif xpos >= apos and ypos >= bpos:
            coordinates[0] = apos
            coordinates[1] = bpos
            coordinates[2] = xpos
            coordinates[3] = ypos
        elif xpos <= apos and ypos >= bpos:
            coordinates[0] = xpos
            coordinates[1] = bpos
            coordinates[2] = apos
            coordinates[3] = ypos
        elif xpos >= apos and ypos <= bpos:
            coordinates[0] = apos
            coordinates[1] = ypos
            coordinates[2] = xpos
            coordinates[3] = bpos
        self.displayCoordinates(coordinates)

        
    def loadNeedle(self, arg):
        """Load the existing needle information from the file and display them in the window."""
        if self.imageName != None:
            jsonfile = self.returnPath(self.imageName).replace(".png", ".json")
            self.handler = fileHandler(jsonfile)
            self.handler.readFile()
            jsondata = self.handler.provideData()

            self.needle = needleData(jsondata)
            properties = self.needle.provideProperties()
            self.propText.delete("1.0", "end")
            self.propText.insert("end", properties)
            tags = self.needle.provideTags()
            self.textField.delete("1.0", "end")
            self.textField.insert("end", tags)
            json = self.needle.provideJson()
            self.textJson.delete("1.0", "end")
            self.textJson.insert("end", json)
            areas = self.needle.provideAreaCount()
            self.needleEntry.delete(0, "end")
            self.needleEntry.insert(0, areas)
            if self.rectangle != None:
                self.pictureField.delete(self.rectangle)
                self.rectangle = None
            self.showArea(None)
        else:
            messagebox.showerror("Error", "No images are loaded. Select image directory first.")

    def createNeedle(self, arg):
        """Write out the json file for the actual image to store the needle permanently."""
        jsondata = self.needle.provideJson()
        filename = self.nameEntry.get().replace(".png", ".json")
        path = self.returnPath(filename)
        if self.handler == None:
            self.handler = fileHandler(path)
        self.handler.acceptData(jsondata)
        self.handler.writeFile(path)
        self.pictureField.delete(self.rectangle)
        self.rectangle = None

#-----------------------------------------------------------------------------------------------

class fileHandler:
    def __init__(self, jsonfile):
        self.jsonData = {"properties": [],
                         "tags": [],
                         "area": []}
        self.jsonfile = jsonfile

    def readFile(self):
        """Read the json file and create the data variable with the info."""
        try:
            with open(self.jsonfile, "r") as inFile:
                self.jsonData = json.load(inFile)
        except FileNotFoundError:
            if self.jsonfile != "empty":
                messagebox.showerror("Error", "No needle exists. Create one.")
            else:
                messagebox.showerror("Error", "No images are loaded. Select image directory.")

    def writeFile(self, jsonfile):
        """Take the data variable and write is out as a json file."""
        with open(jsonfile, "w") as outFile:
            json.dump(self.jsonData, outFile, indent=2)
        messagebox.showinfo("Info", "The needle has been written out.")

    def provideData(self):
        """Provide the json file."""
        return self.jsonData

    def acceptData(self, jsondata):
        """Update the data in data variable."""
        self.jsonData = jsondata

class needleData:
    def __init__(self, jsondata):
        self.jsonData = jsondata
        self.areas = self.jsonData["area"]
        self.areaPos = 0

    def provideJson(self):
        """Provide the json data (for the GUI)."""
        return self.jsonData

    def provideProperties(self):
        """Provide properties."""
        properties = "\n".join(self.jsonData["properties"])
        return properties
    
    def provideTags(self):
        """Provide tags."""
        tags = "\n".join(self.jsonData["tags"])
        return tags
    
    def provideNextArea(self):
        """Provide information about the active area and move pointer to the next area for future reference."""
        try:
            area = self.areas[self.areaPos]
            xpos = area["xpos"]
            ypos = area["ypos"]
            wide = area["width"]
            high = area["height"]
            typ = area["type"]
            apos = xpos + wide
            bpos = ypos + high
            areaData = [xpos, ypos, apos, bpos, typ]
            self.areaPos += 1
            return areaData
        except IndexError:
            messagebox.showerror("Error", "No more area in the needle.")

    def update(self, coordinates, tags, props):
        """Update all information taken from the GUI in the data variable."""
        xpos = coordinates[0]
        ypos = coordinates[1]
        apos = coordinates[2]
        bpos = coordinates[3]
        typ = coordinates[4]
        wide = int(apos) - int(xpos)
        high = int(bpos) - int(ypos)
        area = {"xpos":xpos, "ypos":ypos, "width":wide, "height":high, "type":typ}
        if type(props) != list:
            props = [props]
        if type(tags) != list:
            tags = [tags]
        self.jsonData["properties"] = props
        self.jsonData["tags"] = tags
        
        try:
            self.areas[self.areaPos-1] = area
        except IndexError:
            messagebox.showerror("Error", "Cannot modify non-existent area. Add area first!")
        self.jsonData["area"] = self.areas
            
    def addArea(self):
        """Add new area to the needle (at the end of the list)."""
        self.areas.append("newarea")
        self.areaPos = len(self.areas)

    def removeArea(self):
        """Remove the active area from the area list."""
        try:
            deleted = self.areas.pop(self.areaPos-1)
            self.jsonData["area"] = self.areas
            self.areaPos -= 2
        except IndexError:
            messagebox.showerror("Error", "No area in the needle. Not deleting anything.")

    def provideAreaCount(self):
        """Provide the number of the areas in the needle."""
        return len(self.areas)


#-----------------------------------------------------------------------------------------------

root = tk.Tk()
root.title("Python Needle Editor for OpenQA (Version 0.99)")

app = Application(root)

root.mainloop()
root.destroy() # optional; see description below

