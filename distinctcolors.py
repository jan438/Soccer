import os
import sys
import csv
import math
import unicodedata
from pathlib import Path
from datetime import datetime, date, timedelta
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np

socfont = "LiberationSerif"
   
nationsdata = []
xcolors = []
wccolorstodo = []
eccolors = []

def lookupcolor(color):
    index = -1
    for l in range(len(xcolors)):
        if xcolors[l][0] == color:
            index = l
    return index
    
def get_distinct_colors(n):
    """
    Generate up to n visually distinct colors as HEX codes.
    Uses Tableau, CSS4, and fallback HSV spacing if needed.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Number of colors must be a positive integer.")

    # Start with Tableau colors (highly distinguishable)
    tableau_colors = list(mcolors.TABLEAU_COLORS.values())

    # Add CSS4 named colors (sorted for consistency)
    css4_colors = list(mcolors.CSS4_COLORS.values())

    # Combine and remove duplicates while preserving order
    seen = set()
    unique_colors = []
    for c in tableau_colors + css4_colors:
        if c not in seen:
            seen.add(c)
            unique_colors.append(c)

    # If more colors are needed, generate from HSV evenly spaced
    if n > len(unique_colors):
        extra_needed = n - len(unique_colors)
        hsv_colors = [
            mcolors.to_hex(plt.cm.hsv(i / extra_needed))
            for i in range(extra_needed)
        ]
        unique_colors.extend(hsv_colors)

    return unique_colors[:n]

if sys.platform[0] == 'l':
    path = '/home/jan/git/Soccer'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Soccer"
os.chdir(path)
pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
file_to_open = "Data/WC2026.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        nationsdata.append(row)
        #print(row[12])
        count += 1
print("Count csv", count)

file_to_open = "Data/xkcdrgb.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        xcolors.append(row)
        count += 1
print("Count csv", count)

file_to_open = "Data/EC2015.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        eccolors.append(row)
        count += 1
print("Count csv", count)

file_to_open = "Data/wccolorstodo.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        wccolorstodo.append(row)
        count += 1
print("Count csv", count)

my_canvas = canvas.Canvas("PDF/distinctcolors.pdf")
my_canvas.setTitle("Distinct Colors")
my_canvas.setFont(socfont, 20)
my_canvas.drawString(200, 805, "Distinct Colors")
colors_48 = get_distinct_colors(48)
left_padding = 5
matplot_y = 605
fifty_y = 605
eccolors_y = 405
wccolorstodo_y = 205
wccolors_y = 5
width = 45
height = 45
i = 0
my_canvas.setFont(socfont, 20)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, matplot_y + 4.02 * height, "MatPlot" )
for row in range(4):
   for col in range(12):
       my_canvas.setFillColor(HexColor(colors_48[i]))
       my_canvas.rect(left_padding + col * width, matplot_y + row * height, width, height, fill = 1)
       i += 1
i = 0
my_canvas.setFont(socfont, 20)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, eccolors_y + 4.02 * height, "ECColors" )
for row in range(4):
   for col in range(12):
       if i == 52:
           break
       eccolor = eccolors[i][1]
       ecname = eccolors[i][0]
       my_canvas.setFillColor(HexColor(eccolor))
       my_canvas.rect(left_padding + col * width, eccolors_y + row * height, width, height, fill = 1)
       my_canvas.setFont(socfont, 8)
       if eccolor < '#800000':
           my_canvas.setFillColor(HexColor("#ffffff"))
           my_canvas.drawString(left_padding + col * width + 5, eccolors_y + row * height + 5, ecname)
       else:
           my_canvas.setFillColor(HexColor("#000000"))
           my_canvas.drawString(left_padding + col * width + 5, eccolors_y + row * height + 5, ecname)
       i += 1       
i = 0
my_canvas.setFont(socfont, 20)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, wccolorstodo_y + 4.02 * height, "WCColorsTodo" )
for row in range(4):
   for col in range(12):
       wccolor = wccolorstodo[i][0]
       colorindex = lookupcolor(wccolor)
       if colorindex >= 0:
           my_canvas.setFillColor(HexColor(xcolors[colorindex][1]))
           my_canvas.rect(left_padding + col * width, wccolorstodo_y + row * height, width, height, fill = 1)
           my_canvas.setFont(socfont, 8)
           my_canvas.setFillColor(HexColor("#000000"))
           my_canvas.drawString(left_padding + col * width + 5, wccolorstodo_y + row * height + 5, xcolors[colorindex][0])
       else:
           my_canvas.setFillColor(HexColor("#000000"))
           my_canvas.rect(left_padding + col * width, wccolorstodo_y + row * height, width, height, fill = 1)
       i += 1
i = 0
my_canvas.setFont(socfont, 20)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, wccolors_y + 4.02 * height, "WCColors" )
for row in range(4):
    for col in range(12):
        nationcolorname = nationsdata[i][9]
        colorindex = lookupcolor(nationcolorname)
        if colorindex >= 0:
            nationcolor = xcolors[colorindex][1]
            my_canvas.setFillColor(HexColor(nationcolor))
            my_canvas.rect(left_padding + col * width, wccolors_y + row * height, width, height, fill = 1)
            my_canvas.setFont(socfont, 8)
            if nationcolor < '#800000':
                my_canvas.setFillColor(HexColor("#ffffff"))
                my_canvas.drawString(left_padding + col * width + 5, wccolors_y + row * height + 5, nationcolorname)
            else:
                my_canvas.setFillColor(HexColor("#000000"))
                my_canvas.drawString(left_padding + col * width + 5, wccolors_y + row * height + 5, nationcolorname)
        else:
            my_canvas.setFillColor(HexColor("#000000"))
            my_canvas.rect(left_padding + col * width, wccolors_y + row * height, width, height, fill = 1)
        i += 1
my_canvas.save()
key = input("Wait")
