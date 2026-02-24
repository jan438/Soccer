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
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import xml.etree.ElementTree as ET

def scaleSVG(svgfile, scaling_factor):
    svg_root = load_svg_file(svgfile)
    #print("root", dir(svg_root))
    svgRenderer = SvgRenderer(svgfile)
    drawing = svgRenderer.render(svg_root)
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing
    
def png(svg,pngfilename):
    text_file = open("template.svg", "w")
    text_file.write(svg)
    text_file.close()
    drawing = svg2rlg("template.svg")
    renderPM.drawToFile(drawing, pngfilename)
    
if sys.platform[0] == 'l':
    path = '/home/jan/git/Soccer'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Soccer"
os.chdir(path)
tree = ET.parse('Germany.svg')
root = tree.getroot()
tag = root.tag
attrib = root.attrib
for value in attrib.items():
    print(value)
    break
drawing = scaleSVG("Germany.svg", 1.0)
renderPDF.drawToFile(drawing, "PDF/Germany.pdf")
svgtemplate="""
<svg   width="1250" height="1250"  viewBox="-40 -40 80 80">
<rect width="30" height="30" style="fill:red" />
</svg>
"""
png(svgtemplate,'PDF/Test_viewBox.png')
key = input("Wait")
