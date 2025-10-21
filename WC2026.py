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
version = "1.0"
nationsdata = []

def scaleSVG(svgfile, scaling_factor):
    svg_root = load_svg_file(svgfile)
    svgRenderer = SvgRenderer(svgfile)
    drawing = svgRenderer.render(svg_root)
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing

if sys.platform[0] == 'l':
    path = '/home/jan/git/Soccer'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Soccer"
os.chdir(path)
file_to_open = "Data/WC2026.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        nationsdata.append(row)
        count += 1
print("Count csv", count)

# 595 pixels = 210 mm A4 width, 842 pixels = 297 mm A4 height
# north-america svg width="1000" height="902" scaled 0.5 = 500 x 451

left_padding = 0
bottom_padding = 0
width = 595
height = 842
poule_width = 48
poule_height = 200
pouleland_height = 40
outsidearea = "#9e9e9e"
left_margin = 9.4
poulerect_y = 590
teamspp = 4
poule_x = left_margin
pouleland_y = 730
poule_margin = 5

countnations = 48

pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
my_canvas = canvas.Canvas("PDF/WorldCup2026.pdf")

my_canvas.setTitle("World Cup 2026")

my_canvas.setFillColor(HexColor(outsidearea))
my_canvas.rect(left_padding, bottom_padding, width, height, fill = 1)

drawing = scaleSVG('SVG/north-america.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 0, 100)
drawing = scaleSVG('FIFA.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 50, 800)

my_canvas.setFont(socfont, 25)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.setTitle("World Cup Soccer 2026 " + version)
my_canvas.drawString(200, 805, "World Cup Soccer 2026")

teamcounter = 0
my_canvas.setStrokeColor(black)
for poule in range(12):
    my_canvas.setFont(socfont, 20)
    my_canvas.setFillColor(HexColor("#000000"))
    my_canvas.drawString(left_margin + poule * poule_width, poulerect_y + poule_height - 17, chr(65 + poule))
    my_canvas.rect(left_margin + poule * poule_width, poulerect_y, poule_width, poule_height, stroke = 1, fill = 0)
    for team in range(teamspp):
        nameinlogo = nationsdata[teamcounter][4]
        my_canvas.setFillColor(HexColor("#c5c5c5"))
        my_canvas.rect(left_margin + poule * poule_width + poule_margin, pouleland_y, poule_width - 2 * poule_margin, pouleland_height, stroke = 1, fill = 1)
        drawing = scaleSVG("Logos/" + nationsdata[teamcounter][0] + ".svg", float(nationsdata[teamcounter][1]))
        renderPDF.draw(drawing, my_canvas, poule_x + float(nationsdata[teamcounter][2]), pouleland_y +  float(nationsdata[teamcounter][3]))
        if nameinlogo[0] == "n":
            my_canvas.setFillColor(HexColor("#000000"))
            my_canvas.setFont(socfont, 8)
            my_canvas.drawString(left_margin + poule * poule_width + 4, pouleland_y + 1, nationsdata[teamcounter][0])
        pouleland_y = pouleland_y - (pouleland_height + poule_margin)
        teamcounter += 1
    poule_x = poule_x + poule_width
    pouleland_y = 730

my_canvas.save()
key = input("Wait")
