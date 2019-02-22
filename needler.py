#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23  08:46:48 2019

@author: Lukáš Růžička (lruzicka@redhat.com)
"""

import tkinter as tk
import os
import sys
import subprocess
from tkinter import filedialog, messagebox
from PIL import Image

class Application:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.grid()
        self.buildWidgets()
        self.fileCounter = 0
        self.wdirContent = os.listdir()

    def buildWidgets(self):
        self.vmDesc = tk.Label(self.frame, text="Name of VM domain:")
        self.vmDesc.grid(row=0, column=0, sticky="news")

        self.vmEntry = tk.Entry(self.frame, width=30)
        self.vmEntry.grid(row=0, column=1, sticky="news")
        
        self.fileDesc = tk.Label(self.frame, text="Name of output file:")
        self.fileDesc.grid(row=1, column=0, sticky="news")

        self.fileEntry = tk.Entry(self.frame, width=30)
        self.fileEntry.grid(row=1, column=1, sticky="news")

        self.saveButton = tk.Button(self.frame, text="Take screenshot", width=15, command=self.takeScreenshot)
        self.saveButton.grid(row=2, column=0, sticky="news")

        self.quitButton = tk.Button(self.frame, text="Quit", width=15, command=self.frame.quit)
        self.quitButton.grid(row=2, column=1, sticky="news")


    def takeScreenshot(self):
        vmName = self.vmEntry.get()
        fileName = self.fileEntry.get()
        if fileName == '':
            fileName = str(self.fileCounter)
            while f"{fileName}.ppm" in self.wdirContent:
                fileName = str(int(fileName)+1)
                self.wdirContent = os.listdir()
        
        self.fileEntry.delete(0, "end")
        outfile = f"{fileName}.ppm"
        cfile = f"{fileName}.png"
        sshot = f"virsh screenshot {vmName} {outfile}"
        code = os.system(sshot)
        if code != 0:
            messagebox.showerror("Error", "The screenshot could not be taken. Make sure the VM domain name is correct. If so, try to run the program with sudo.")
            print("Error, the screenshot could not be taken.")
        convert = f"convert {outfile} {cfile}"
        code = os.system(convert)
        if code != 0:
            messagebox.showerror("Error", "The file could not be converted. Is ImageMagick installed?")
            print("Conversion error")

#--------------------------------------------------------------------


root = tk.Tk()
root.title("Python Screenshot for OpenQA (Version 0.99)")

app = Application(root)

root.mainloop()
root.destroy() # optional; see description below
