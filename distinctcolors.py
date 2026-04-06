import os
import sys
import csv
import math
import unicodedata
from pathlib import Path
from datetime import datetime, date, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np

colors = [
"#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438","#A8A202","#158FAD","#14AAF5","#CD0027",
"#4073FF","#D38895","#884DFF","#AF38EB","#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438",
"#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438","#A8A202","#158FAD","#14AAF5","#CD0027",
"#4073FF","#D38895","#884DFF","#AF38EB","#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438",
          ]
          
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
my_canvas = canvas.Canvas("PDF/distinctcolors.pdf")
colors_48 = get_distinct_colors(48)
for i in range(48):
    print(colors_48[i])
left_padding = 100
bottom_padding = 300
width = 40
height = 40
i = 0
for row in range(4):
   for col in range(12):
       my_canvas.setFillColor(HexColor(colors[i]))
       my_canvas.rect(left_padding + col * width, bottom_padding + row * height, width, height, fill = 1)
       i += 1
my_canvas.save()
key = input("Wait")
