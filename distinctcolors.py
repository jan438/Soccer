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
left_padding = 10
bottom_padding = 100
width = 10
height = 10
my_canvas.rect(left_padding, bottom_padding, width, height, fill = 1)
my_canvas.save()
key = input("Wait")
