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

if sys.platform[0] == 'l':
    path = '/home/jan/git/Soccer'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Soccer"
os.chdir(path)
my_canvas = canvas.Canvas("PDF/distinctcolors.pdf")
my_canvas.setFillColor(HexColor('#FECDE5'))
left_padding = 100
bottom_padding = 300
width = 40
height = 40
for col in range(12):
   for row in range(4):
       my_canvas.rect(left_padding + col * width, bottom_padding + row * height, width, height, fill = 1)
my_canvas.save()
key = input("Wait")
