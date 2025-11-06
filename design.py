import os
import calendar
from datetime import datetime, date, timedelta
import pytz
import os
import sys
import csv
import math
import unicodedata
from ics import Calendar, Event
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.colors import blue, green, black, red, pink, gray, brown, purple, orange, yellow, white, lightgrey
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, mm
from reportlab.graphics.shapes import *
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer

socfont = "LiberationSerif"
Borealis = [ "#01EFAC", "#01CBAE", "#2082A6", "#524094", "#562A83" ]
BluePlanet1 = [ "#2297FA", "#50B6FE", "#7ED8FA", "#94AEFE", "#8082D6" ]
Oasis = [ "#23570D", "#367C28", "#86B06B", "#BAD5EC", "#6BA2DE" ]

design_x = 10
design_y = 800
width = 50
height = 50

if sys.platform[0] == 'l':
    path = '/home/jan/git/Soccer'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Soccer"
os.chdir(path)

pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
my_canvas = canvas.Canvas("PDF/Designs.pdf")

my_canvas.setTitle("Designs")

my_canvas.setFillColor(HexColor(Borealis[0]))
my_canvas.rect(design_x, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(Borealis[1]))
my_canvas.rect(design_x + width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(Borealis[2]))
my_canvas.rect(design_x + 2 * width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(Borealis[3]))
my_canvas.rect(design_x + 3 * width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(Borealis[4]))
my_canvas.rect(design_x + 4 * width, design_y, width, height, fill = 1)
design_y = design_y - 50
my_canvas.setFillColor(HexColor(BluePlanet1[0]))
my_canvas.rect(design_x, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(BluePlanet1[1]))
my_canvas.rect(design_x + width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(BluePlanet1[2]))
my_canvas.rect(design_x + 2 * width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(BluePlanet1[3]))
my_canvas.rect(design_x + 3 * width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(BluePlanet1[4]))
my_canvas.rect(design_x + 4 * width, design_y, width, height, fill = 1)
design_y = design_y - 50
my_canvas.setFillColor(HexColor(Oasis[0]))
my_canvas.rect(design_x, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(Oasis[1]))
my_canvas.rect(design_x + width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(Oasis[2]))
my_canvas.rect(design_x + 2 * width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(Oasis[3]))
my_canvas.rect(design_x + 3 * width, design_y, width, height, fill = 1)
my_canvas.setFillColor(HexColor(Oasis[4]))
my_canvas.rect(design_x + 4 * width, design_y, width, height, fill = 1)

my_canvas.save()
key = input("Wait")
