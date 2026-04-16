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

target_colors = [
# aqua2        aquamarine          azure         beige              blue               brown        chartreuse
"#13EAC9","#04D8B2","#7FFFD6","#069AF3","#F5F5DC","#E6DAA6","#0000FF","#0343DF","#A52A2A","#653700","#7FFF00","#C1F80A",
#   chocolate              coral               crimson         darkblue              darkgreen  yellowfuchsia
"#D2691E","#3D1C02","#FF7F50","#FC5A50","#DC143C","#8C000F","#00008B","#030764","#006400","#054907","#FFFF14","#ED0Dd9",
#    gold                   goldenrod          green             silver               indigo           khaki
"#FFD700","#DBB40C","#DAA520","#FAC205","#008000","#15B01A","#808080","#929591","#4B0082","#380282","#F0E68C","#AAA662",
#     lavendar             lightblue          lightgreen           lime               magenta          maroon
"#E6E6FA","#C79FEF","#ADD8E6","#7BC8F6","#90EE90","#76FF7B","#00FF00","#AAFF32","#FFA500","#C20078","#800000","#650021",
          ]   
            
nationsdata = []
xcolors = []
wccolors = []

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

file_to_open = "Data/wccolorstodo.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        wccolors.append(row)
        count += 1
print("Count csv", count)

my_canvas = canvas.Canvas("PDF/distinctcolors.pdf")
colors_48 = get_distinct_colors(48)

left_padding = 5
matplot_y = 650
target_y = 450
wccolors_y = 250
custom_y = 50
width = 45
height = 45
i = 0
my_canvas.setFont(socfont, 25)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, matplot_y + 4.3 * height, "MatPlot" )
for row in range(4):
   for col in range(12):
       my_canvas.setFillColor(HexColor(colors_48[i]))
       my_canvas.rect(left_padding + col * width, matplot_y + row * height, width, height, fill = 1)
       i += 1
i = 0
my_canvas.setFont(socfont, 25)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, target_y + 4.3 * height, "Target" )
for row in range(4):
   for col in range(12):
       my_canvas.setFillColor(HexColor(target_colors[i]))
       my_canvas.rect(left_padding + col * width, target_y + row * height, width, height, fill = 1)
       i += 1
i = 0
my_canvas.setFont(socfont, 25)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, wccolors_y + 4.3 * height, "WCColorsTodo" )
for row in range(4):
   for col in range(12):
       wccolor = wccolors[i][0]
       colorindex = lookupcolor(wccolor)
       if colorindex >= 0:
           my_canvas.setFillColor(HexColor(xcolors[colorindex][1]))
           my_canvas.rect(left_padding + col * width, wccolors_y + row * height, width, height, fill = 1)
           my_canvas.setFont(socfont, 8)
           my_canvas.setFillColor(HexColor("#000000"))
           my_canvas.drawString(left_padding + col * width + 5, wccolors_y + row * height + 5, xcolors[colorindex][0])
       else:
           my_canvas.setFillColor(HexColor("#000000"))
           my_canvas.rect(left_padding + col * width, wccolors_y + row * height, width, height, fill = 1)
       i += 1
i = 0
my_canvas.setFont(socfont, 25)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, custom_y + 4.3 * height, "WCColors" )
for row in range(4):
    for col in range(12):
        nationcolorname = nationsdata[i][9]
        colorindex = lookupcolor(nationcolorname)
        if colorindex >= 0:
            nationcolor = xcolors[colorindex][1]
            my_canvas.setFillColor(HexColor(nationcolor))
            my_canvas.rect(left_padding + col * width, custom_y + row * height, width, height, fill = 1)
            my_canvas.setFont(socfont, 8)
            if nationcolor < '#800000':
                my_canvas.setFillColor(HexColor("#ffffff"))
                my_canvas.drawString(left_padding + col * width + 5, custom_y + row * height + 5, nationcolorname)
            else:
                my_canvas.setFillColor(HexColor("#000000"))
                my_canvas.drawString(left_padding + col * width + 5, custom_y + row * height + 5, nationcolorname)
        else:
            my_canvas.setFillColor(HexColor("#000000"))
            my_canvas.rect(left_padding + col * width, custom_y + row * height, width, height, fill = 1)
        i += 1
my_canvas.save()
key = input("Wait")
