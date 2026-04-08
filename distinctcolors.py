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

#   1f77b4
#   ff7f0e
#   2ca02c
#   d62728
#   9467bd
#   8c564b
#   e377c2
#   7f7f7f
#   bcbd22
#   17becf
#   F0F8FF
#   FAEBD7

#   00FFFF
#   7FFFD4
#   F0FFFF
#   F5F5DC
#   FFE4C4
#   000000
#   FFEBCD
#   0000FF
#   8A2BE2
#   A52A2A
#   DEB887
#   5F9EA0

#   7FFF00
#   D2691E
#   FF7F50
#   6495ED
#   FFF8DC
#   DC143C
#   00008B
#   008B8B
#   B8860B
#   A9A9A9
#   006400
#   BDB76B

#   8B008B
#   556B2F
#   FF8C00
#   9932CC
#   8B0000
#   E9967A
#   8FBC8F
#   483D8B
#   2F4F4F
#   00CED1
#   9400D3
#   FF1493

colors = [
"#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438","#A8A202","#158FAD","#14AAF5","#CD0027",
"#4073FF","#D38895","#884DFF","#AF38EB","#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438",
"#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438","#A8A202","#158FAD","#14AAF5","#CD0027",
"#4073FF","#D38895","#884DFF","#AF38EB","#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438",
          ]
          
target_colors = [
# aqua        aquamarine          azure         beige              blue               brown        chartreuse
"#13EAC9","#04D8B2","#7FFFD6","#069AF3","#F5F5DC","#E6DAA6","#0000FF","#0343DF","#A52A2A","#653700","#7FFF00","#C1F80A",
#   chocolate              coral               crimson         darkblue              darkgreen      fuchsia
"#D2691E","#3D1C02","#FF7F50","#FC5A50","#DC143C","#8C000F","#00008B","#030764","#006400","#054907","#FF00FF","#ED0Dd9",
#    gold                   goldenrod          green             silver
"#FFD700","#DBB40C","#DAA520","#FAC205","#008000","#15B01A","#808080","#929591","#A8A202","#158FAD","#14AAF5","#CD0027",
"#4073FF","#D38895","#884DFF","#AF38EB","#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438",
          ]         
          
nationsdata = []
     
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
my_canvas = canvas.Canvas("PDF/distinctcolors.pdf")
colors_48 = get_distinct_colors(48)
for i in range(48):
    print(colors_48[i])
    colors[i] = colors_48[i]
left_padding = 100
matplot_y = 500
target_y = 300
custom_y = 100
width = 40
height = 40
i = 0
my_canvas.setFont(socfont, 25)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.drawString(left_padding, matplot_y + 4.3 * height, "MatPlot" )
for row in range(4):
   for col in range(12):
       my_canvas.setFillColor(HexColor(colors[i]))
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
my_canvas.drawString(left_padding, custom_y + 4.3 * height, "Custom" )
for row in range(4):
   for col in range(12):
       my_canvas.setFillColor(HexColor(nationsdata[i][9]))
       my_canvas.rect(left_padding + col * width, custom_y + row * height, width, height, fill = 1)
       i += 1
my_canvas.save()
key = input("Wait")
