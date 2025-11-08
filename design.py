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
designs = [[ "Borealis", "#01EFAC", "#01CBAE", "#2082A6", "#524094", "#562A83", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "BluePlanet1", "#2297FA", "#50B6FE", "#7ED8FA", "#94AEFE", "#8082D6" , "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Oasis", "#23570D", "#367C28", "#86B06B", "#BAD5EC", "#6BA2DE", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Black Forest", "#0E1609", "#1D2C20", "#2E462B", "#5C6D5E", "#A0A899", "#ffffff", "#ffffff", "#ffffff", "#000000", "#000000"],
           [ "Butterfly Blue", "#3173D7", "#50BFDB", "#A6E4DD", "#6F9CDC", "#7270DD", "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Arctic", "#83A7C9", "#A2C6E8", "#E0ECF8", "#6ACCF3", "#2094D1" , "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Verdant", "#76C474", "#4FB65E", "#1D9642", "#116630", "#063009" , "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Icecap", "#777DB4", "#99B5F4", "#709FEB", "#3765A9", "#08386E", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Turquoise Torrent", "#6ED1D4", "#87EAE5", "#B1EDEF", "#A4D9EB", "#84CEE9", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Alaska", "#5E436C", "#7D648E", "#D5DAE3", "#87A4DE", "#5873CB", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Blooms in Blue", "#427938", "#4DA73D", "#488872", "#359DED", "#0282C9", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Clear Cobalt", "#D6F0F1", "#9DCCD7", "#5997AE", "#165578", "#0F151D", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Crystalline", "#002D3F", "#024A65", "#015E80", "#016A8E", "#047A9A", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Blue Ridge", "#DCF2FD", "#BBE6F9", "#596BB3", "#1E386B", "#102447", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Jungle", "#4E785E", "#2A4B44", "#24342A", "#131C1B", "#4C5C65", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Coral Cove", "#0B4746", "#085B5B", "#17A8B1", "#3FD5DE", "#1EE9F2", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Fields of Lavender", "#2E2462", "#4D5082", "#51645C", "#376F91", "#113C5F", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Caribbean Coast", "#16505B", "#20646D", "#2D8181", "#8EAF82", "#255A00" , "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Northern Lights", "#4BCFD6", "#1A5092", "#346EA4", "#3D8FB1", "#A7DCEF", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Bluebells", "#5A619A", "#6785CC", "#8697CA", "#87B77B", "#67A45F", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Moonstone", "#016FAE", "#6BE6CF", "#019DAC", "#01697C", "#015649", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Ursa Major", "#075A77", "#079BBB", "#13B8CE", "#6D79C2", "#512475", "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Paradise", "#01374A", "#0395A7", "#72ADBF", "#5E877D", "#2B5435", "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Little Pigeon", "#0A1932", "#143151", "#617997", "#9BB6DA", "#DFF0FD", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Amethyst Freeze", "#332686", "#523DC5", "#375ED2", "#BEF4FE", "#289991", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Lakeshore", "#122C41", "#08445B", "#2E647A", "#2185B6", "#035042", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Fly by Night", "#433E76", "#514F81", "#65779D", "#819CBA", "#AFBCCE", "#000000", "#000000", "#000000", "#000000", "#000000"],
           [ "Blue Agate", "#264248", "#398A95", "#DCE2E5", "#60BDBC", "#1B7979", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Equator", "#01697C", "#01B1C6", "#01E7DC", "#00C2A5", "#00785B", "#000000", "#000000", "#000000", "#000000", "#000000" ],
           [ "Skyline", "#038492", "#05B2C7", "#5D4CDA", "#3995E9", "#0473AD", "#000000", "#000000", "#000000", "#000000", "#000000" ]]

design_x = 10
design_y = 700
width = 32
height = 32
abcdy = 23
abcdx = 8

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

for i in range(len(designs)):
    my_canvas.setFillColor(black)
    my_canvas.drawString(design_x, design_y + 33, designs[i][0])
    
    my_canvas.setFillColor(HexColor(designs[i][1]))
    my_canvas.rect(design_x, design_y, width, height, stroke = 0, fill = 1)
    my_canvas.setFillColor(designs[i][6])
    my_canvas.drawString(design_x + abcdx, design_y + abcdy, "abc" )
    
    my_canvas.setFillColor(HexColor(designs[i][2]))
    my_canvas.rect(design_x + width, design_y, width, height, stroke = 0, fill = 1)
    my_canvas.setFillColor(designs[i][7])
    my_canvas.drawString(design_x + width + abcdx, design_y + abcdy, "abc" )
    
    my_canvas.setFillColor(HexColor(designs[i][3]))
    my_canvas.rect(design_x + 2 * width, design_y, width, height, stroke = 0, fill = 1)
    my_canvas.setFillColor(designs[i][8])
    my_canvas.drawString(design_x + 2 * width + abcdx, design_y + abcdy, "abc" )
    
    my_canvas.setFillColor(HexColor(designs[i][4]))
    my_canvas.rect(design_x + 3 * width, design_y, width, height, stroke = 0, fill = 1)
    my_canvas.setFillColor(designs[i][9])
    my_canvas.drawString(design_x + 3 * width + abcdx, design_y + abcdy, "abc" )
    
    my_canvas.setFillColor(HexColor(designs[i][5]))
    my_canvas.rect(design_x + 4 * width, design_y, width, height, stroke = 0, fill = 1)
    my_canvas.setFillColor(designs[i][10])
    my_canvas.drawString(design_x + 4 * width + abcdx, design_y + abcdy, "abc" )
    
    design_y = design_y - 50
    if i == 9 or i == 19:
        design_x += 185
        design_y = 700
    
my_canvas.save()
key = input("Wait")
