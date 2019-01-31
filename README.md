# Python Needle Editor for creating OpenQA needles (Version 0.99)

The Needle Editor creates and modifies needles for the OpenQA tests. The advantage of the editor is
that it does not need OpenQA to be installed on the system. Only screenshots upon which the needles 
will be created are needed. With the editor, the needles can be made in advance and then only tested finally in the OpenQA 
instance. 

The editor only supports *png* screenshots, however if a *json* needle description already exists for a particular image,
you can load that instead and a correct image will load. 

## Requirements

* Python 3
* Tkinter
* the Pillow library

## Using the editor

### Starting the editor

The editor is started from the console. You can start it in two ways:

* When started *without arguments*, the editor opens without any image loaded. To work with it, at least one image must be loaded first.
* The editor can be started *with a path to a file*. In this case, it opens with that particular image loaded, which saves a lot of time when you need to edit a needle quickly.


### Reading the images

#### Editing multiple files in a directory

You can open a directory to navigate through images one after another and edit their needles. To use this approach:

1. Click the **Select image directory** button.
2. Use the dialogue to select a directory where the screenshots are located.

**Note:** The editor reports number of images in the directory, when you have selected it.

#### Editing a single file

You can also open a particular file and edit its needle. To use this approach:

1. Click the **Select image file** button or hit the **o** key.
2. Use the dialogue to locate the file you want to edit.


### Navigating through images

You can navigate through the images back and forth in the loop. To navigate through the image loop:

1. Click the **Next picture** or the **Previous picture** buttons.
2. Use the **n** and **p** keys. 


### Working with needles

#### Loading the needle information

When you have navigated to the image you want to create a needle for, make sure you try loading an
existing needle. Not doing so, you could accidentally overwrite it. To load a needle:

1. Click the **Load needle** button or press the **l** key. The needle loads if it exists and the first needle area shows
in the image window.

**Note**: You can load the needle again anytime and restore all the original information until the needle 
has been saved.

#### Reading the needle information.

When the needle is loaded, you can see all needle information in the right part of the program window.
Among others:

* the name of the active image
* needle properties
* needle tags
* active area coordinates
* number of areas in the needle
* the content of the needle json file

#### Updating the needle information
You can manually update the following fields:

* the coordinates
* the properties
* the tags
* the area type

#### Redrawing the area 

The needle area can be updated using several techniqes:

1. You can use the mouse to draw a new needle area. 
2. You can manually update the coordinates in the coordinate fields on the right.
3. You can use keys to change the size of the area. 

When using the keyboard:
	
* Using **Left**, **Right**, **Up**, and **Down** arrows changes the coordinates of the lower right corner in steps of 1 px each.
* Using the **Shift** key combined with arrows changes the coordinates of the upper left corner in steps of 1 px each.
* Holding the **Ctrl** key when pressing arrows increases one step to 5 pxs.
* Holding the **Alt** key when pressing arrows increases one step to 25 pxs.

**Note**: When you have updated the area, you have to click **Modify active area** button 
for them to take effect on the actual needle. 

**Note**: When you have updated the needle fields, the keyboard shortcuts will not work properly because of 
lost focus (known issue). Click into the picture field to get the shortcuts to work again.


#### Saving a needle

If you want to store the needle information permanently, you have to save it. To do so:

1. Click on the **Create needle**, or use the **c** shortcut to save the needle.

When saving, the editor creates a json file (the name of the file matches the name of the active 
image) and stores all needle information in that file. Next time, when you load the needle, the needle information will be restored.

#### Creating a new needle from scratch

To create a new needle, you must provide the required needle information:

* needle tags
* needle area
* needle type (match, ocr, or exclude)
* needle properties (not compulsory)

1. Fill in the necessary information for the properties, type and tags.
2. Draw a rectangle around the area or use any of the approaches from **Redrawing the area** section.
3. Click **Add area to needle** button or press the **a** key to add the area to the needle. See 
*Updating the needle information* to learn about a known issue.
4. If you wish to add another area (the needle can have more areas), just draw a new area and use 
**Step 3** to add it to the needle.
5. If you change the properties, type or tags, then the whole needle will be affected by the change.
6. Click the **Create needle** button to save the needle permanently into a json file.

### Working with areas

#### Add an area to the needle

In order to have an area on the needle, you have to add it to it:

1. Press the **Add area to needle** button (**a**) to add the area to the needle. 
2. Repeat for another area.

You can see the number of areas in the field in the lower right part of the window.

#### Removing an active area

When your area is still active (that means that you have not added a new area yet), it can be removed
from the needle again:

1. Click on the **Remove from needle** button (**r**) to remove it from the needle. 

When removing the area from the needle, the active area falls back to the previous area 
(which becomes active) and the rectangle will show its current position. You can repeat the action,
until all areas are deleted.

#### Showing next area

When the needle has more than one area (you can see the number in the lower right part of the
program window), only the first area is shown. To see the next area:

1. Click on the **Show next area** button (**s**). 

This will show the next area in the needle and makes it active. You can update the area or remove it.

**Warning**: In this version, you cannot navigate in areas. You only can move to the next ones.
However, if you remove the area from the needle, the editor will fall back to the previous area and 
make it active again so you can update or remove it.

If you need to change the first area without removing the next area, use the following workaround:

1. Save the needle (**c**).
2. Load the needle (**l**).
3. Now, the editor makes the very first area active and you can modify it (**m**).
4. Move to the next area (**s**) to modify it.
5. Repeat until you have modified required areas.
6. Save the needle.


## Reporting a problem

If you experience a problem, open an issue. Or help with the development. Yup, it is opensource!




