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
alleventslines = []
gameevents = []

class GameEvent:
    def __init__(self, summary, day, location, starttime, endtime, month):
        self.summary = summary
        self.day = day
        self.location = location
        self.starttime = starttime
        self.endtime = endtime
        self.month = month
        
def lookuplocation(loc):
    index = -1
    for l in range(len(cities)):
        if cities[l][0] == loc:
            index = l
    return index

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

eventcal = "Calendar/WK2026.ics"
in_file = open(os.path.join(path, eventcal), 'r')
count = 0
lastpos = 0
found = 0
for line in in_file:
    newlinepos = line.find("\t\n")
    lastsubstring = line[lastpos:newlinepos]
    alleventslines.append(lastsubstring)
    count += 1
in_file.close()
print("Count eventslines", len(alleventslines))
for i in range(len(alleventslines)):
    neweventpos = alleventslines[i].find("BEGIN:VEVENT")
    summaryeventpos = alleventslines[i].find("SUMMARY")
    locationeventpos = alleventslines[i].find("LOCATION")
    dtstarteventpos = alleventslines[i].find("DTSTART")
    dtendeventpos = alleventslines[i].find("DTEND")
    endeventpos = alleventslines[i].find("END:VEVENT")
    if neweventpos == 0:
        day = 0
        location = ""
        starttime = 0
        endtime = 0
        month = 0
    if dtstarteventpos == 0:
        eventdtstartstr = alleventslines[i][8:]
        datevaluepos = alleventslines[i].find("VALUE=DATE:")
        if datevaluepos == 8:
            eventdtstartstr = alleventslines[i][19:]
        year = int(eventdtstartstr[:4])
        month = int(eventdtstartstr[4:6])
        day = int(eventdtstartstr[6:8])
        starttime = eventdtstartstr
    if dtendeventpos == 0:
        eventdtendstr = alleventslines[i][6:]
        endtime = eventdtendstr[9:11] + ':' + eventdtendstr[11:13]
    if summaryeventpos == 0:
        summary = alleventslines[i][8:]
    if locationeventpos == 0:
        location = alleventslines[i][9:]
    if endeventpos == 0:
        gameevents.append(GameEvent(summary, day, location, starttime, endtime, month))
print("Count game events", len(gameevents))

# 595 pixels = 210 mm A4 width, 842 pixels = 297 mm A4 height
# north-america svg width="1000" height="902" scaled 0.5 = 500 x 451

#citiescolors = ["#88255F", "#DB4035", "#FF9933", "#FAD000", "#AFB83B", "#7ECC49", "#E7E84F", "#299438", "#A8A202", "#158FAD", "#14AAF5", "#CD0027", "#4073FF", "#D38895", "#884DFF", "#AF38EB", "#EB96EB", "#E05194", "#FF8D85", "#808080", "#FFE001", "#CCAC93", "#9A6324", "#80FF80"]

cities = [["Mexico City", "#88255F", [120.0, 150.0], [120.0, 153.0]],
          ["New York", "#DB4035", [150.0, 230.0], [153.0, 230.0]],
          ["Dallas", "#FF9933", [120.0, 190.0], [120.0, 193.0]],
          ["Kansas City", "#FAD000", [120.0, 200.0], [120.0, 203.0]],
          ["Houston", "#AFB83B", [120.0, 180.0], [120.0, 183.0]],
          ["Atlanta", "#7ECC49", [130.0, 215.0], [133.0, 215.0]],
          ["Los Angeles", "#E7E84F", [65.0, 200.0], [55.0, 200.0]],
          ["Seattle", "#299438", [70.0, 245.0],[60.0, 245.0]],
          ["San Francisco", "#A8A202", [65.0, 205.0],[55.0, 205.0]],
          ["Philadelphia", "#158FAD", [150.0, 225.0],[153.0, 225.0]],
          ["Miami", "#14AAF5", [140.0, 205.0],[143.0, 205.0]],
          ["Boston", "#CD0027", [150.0, 240.0], [153.0, 240.0]],
          ["Vancouver", "#4073FF", [70.0, 250.0], [60.0, 255.0]],
          ["Monterrey", "#D38895", [120.0, 170.0],[120.0, 173.0]], 
          ["Toronto", "#884DFF", [150.0, 245.0], [153.0, 245.0]],
          ["Guadalajara", "#AF38EB", [120.0, 160.0], [120.0, 163.0]]]
left_padding = 0
bottom_padding = 0
width = 595
height = 842
poule_width = 48
poule_height = 205
pouleland_height = 40
outsidearea = "#9e9e9e"
left_margin = 9.4
poulerect_y = 585
teamspp = 4
poule_x = left_margin
poule_margin = 5
cadre_pouleland = False
maxnamewidth = 42.0
scalewiki = 0.56
xwiki = 10
ywiki = 50
scalesimple = 0.33
xsimple = -56
ysimple = 10
#mapversie = "Wiki"
mapversie = "Simple"
colwidthgame = 72

countnations = 48

pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
my_canvas = canvas.Canvas("PDF/WorldCup2026" + mapversie + ".pdf")

my_canvas.setTitle("World Cup 2026")

my_canvas.setFillColor(HexColor(outsidearea))
my_canvas.rect(left_padding, bottom_padding, width, height, fill = 1)

if mapversie == "Wiki":
    drawing = scaleSVG("SVG/WorldMap" + mapversie + ".svg", scalewiki)
    renderPDF.draw(drawing, my_canvas, xwiki, ywiki)
else:
    drawing = scaleSVG("SVG/WorldMap" + mapversie + ".svg", scalesimple)
    renderPDF.draw(drawing, my_canvas, xsimple, ysimple)
    
drawing = scaleSVG('FIFA.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 50, 800)

my_canvas.setFont(socfont, 25)
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.setTitle("World Cup Soccer 2026 " + version)
my_canvas.drawString(200, 805, "World Cup Soccer 2026")

for poule in range(12):
    my_canvas.setFillColor(HexColor("#b1b1b1"))
    my_canvas.rect(left_margin + poule * poule_width, poulerect_y, poule_width, poule_height, stroke = 1, fill = 1)
    
teamcounter = 0
my_canvas.setStrokeColor(black)
for poule in range(12):
    pouleland_y = 725
    my_canvas.setFont(socfont, 20)
    my_canvas.setFillColor(HexColor("#000000"))
    my_canvas.drawString(left_margin + poule * poule_width + 17.0, poulerect_y + poule_height - 17, chr(65 + poule))
    for team in range(teamspp):
        nameinlogo = nationsdata[teamcounter][4]
        if cadre_pouleland:
            my_canvas.setFillColor(HexColor("#c5c5c5"))
            my_canvas.rect(left_margin + poule * poule_width + poule_margin, pouleland_y, poule_width - 2 * poule_margin, pouleland_height, stroke = 1, fill = 1)
        drawing = scaleSVG("Logos/" + nationsdata[teamcounter][0] + ".svg", float(nationsdata[teamcounter][1]))
        renderPDF.draw(drawing, my_canvas, poule_x + float(nationsdata[teamcounter][2]), pouleland_y +  float(nationsdata[teamcounter][3]))
        if nameinlogo[0] == "n":
            my_canvas.setFillColor(HexColor("#000000"))
            my_canvas.setFont(socfont, 8)
            namewidth = pdfmetrics.stringWidth(nationsdata[teamcounter][0], socfont, 8)
            my_canvas.drawString(left_margin + 2 + poule * poule_width + 0.5 * (maxnamewidth - namewidth), pouleland_y + 1, nationsdata[teamcounter][0])
        if nationsdata[teamcounter][8] != "NL":
            drawing = scaleSVG("Flags/" + nationsdata[teamcounter][8] + "tw.svg", 0.3)
            renderPDF.draw(drawing, my_canvas, float(nationsdata[teamcounter][6]), float(nationsdata[teamcounter][7]))
            my_canvas.setFillColor(HexColor("#ffff00"))
            my_canvas.circle(float(nationsdata[teamcounter][6]), float(nationsdata[teamcounter][7]), 2.0, stroke = 0, fill = 1)
        pouleland_y = pouleland_y - (pouleland_height + poule_margin)
        teamcounter += 1
    poule_x = poule_x + poule_width
    
for i in range(len(cities)):
    print(cities[i][0])
    my_canvas.setFillColor(HexColor(cities[i][1]))
    my_canvas.circle(float(cities[i][2][0]), float(cities[i][2][1]), 2.0, stroke = 0, fill = 1)
    my_canvas.setFillColor(HexColor("#000000"))
    my_canvas.setFont(socfont, 7)
    my_canvas.drawString(float(cities[i][3][0]), float(cities[i][3][1]), cities[i][0])
    
calindex = 0
limitcalindex = 22
gameindex = 0

line = 550
for j in range(12):   
    for i in range(8):
        if calindex < limitcalindex:
            print(calindex, gameevents[calindex].summary[5], gameevents[calindex].location)
        drawing = scaleSVG("SVG/calendar-blank.svg", 0.4)
        renderPDF.draw(drawing, my_canvas, left_margin + i * colwidthgame, line)
        my_canvas.setFont(socfont, 7)
        my_canvas.setFillColor(HexColor("#ffffff"))  
        my_canvas.drawString(left_margin + i * colwidthgame + 0.48, line + 9.5, gameevents[calindex].summary[5])
        my_canvas.setFillColor(HexColor("#000000"))  
        my_canvas.drawString(left_margin + i * colwidthgame + 0.45, line + 2.5, "19-7")
        my_canvas.setFont(socfont, 8)    
        my_canvas.drawString(left_margin + i * colwidthgame + 30, line, "Opponent2")
        my_canvas.drawString(left_margin + i * colwidthgame + 30, line + 6, "Opponent1")
        drawing = scaleSVG("Clocks/2030tw.svg", 0.4)
        renderPDF.draw(drawing, my_canvas, left_margin + i * colwidthgame + 15, line)
        if calindex < limitcalindex:
            locidx = lookuplocation(gameevents[calindex].location)
            my_canvas.setFillColor(HexColor(cities[locidx][1]))
            my_canvas.circle(left_margin + i * colwidthgame + 8.0, line + 12.0, 2.0, stroke = 0, fill = 1)
        if calindex < limitcalindex:
            calindex += 1
    line -= 18
    if j == 7:
       line -= 10
    if j == 9:
       line -= 10
    if j == 10:
       line -= 10
    
my_canvas.save()
key = input("Wait")
