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
socfontbold = 'LiberationSerifBold'
version = "1.0"
nationsdata = []
alleventslines = []
gameevents = []

class GameEvent:
    def __init__(self, summary, day, description, location, starttime, endtime, month):
        self.summary = summary
        self.day = day
        self.description = description
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
    
def converttimetztolocalclock(timetz):
    utc_string = timetz
    utc_format = "%Y%m%dT%H%M%S"
    local_tz = pytz.timezone('Europe/Amsterdam')
    utc_dt = datetime.strptime(utc_string, utc_format)
    local_dt = utc_dt
    hour = local_dt.hour
    minute = local_dt.minute
    return [hour, minute]

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
    
def drawVerticalRect(c, x, y, w, h, mode, col1, col2):    
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke = 0)
    if mode == "b":
        c.linearGradient(x, y, x, y + h, (col1, col2, col1), (0, 0.5, 1))
    if mode == "t":
        c.linearGradient(x, y, x, y + h, (col1, col2, col1), (1, 0.5, 0))
    c.restoreState()
    
def drawHorizontalRect(c, x, y, w, h, mode, col1, col2):    
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke = 0)
    if mode == "l":
        c.linearGradient(x, y, x + w, y, (col1, col2, col1), (0, 0.5, 1))
    if mode == "r":
        c.linearGradient(x, y, x + w, y, (col1, col2, col1), (1, 0.5, 0))
    c.restoreState()

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
    descriptioneventpos = alleventslines[i].find("DESCRIPTION")
    locationeventpos = alleventslines[i].find("LOCATION")
    dtstarteventpos = alleventslines[i].find("DTSTART")
    dtendeventpos = alleventslines[i].find("DTEND")
    endeventpos = alleventslines[i].find("END:VEVENT")
    if neweventpos == 0:
        day = 0
        description = ""
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
    if descriptioneventpos == 0:
        description = alleventslines[i][12:]
    if locationeventpos == 0:
        location = alleventslines[i][9:]
    if endeventpos == 0:
        gameevents.append(GameEvent(summary, day, description, location, starttime, endtime, month))
print("Count game events", len(gameevents))

# 595 pixels = 210 mm A4 width, 842 pixels = 297 mm A4 height

colors = ["#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438",
          "#A8A202","#158FAD","#14AAF5","#CD0027","#4073FF","#D38895","#884DFF","#AF38EB"]

cities = [["Mexico City", [87.0, 168.0], [87.0, 171.0]],
          ["New York", [145.0, 216.0], [148.0, 213.0]],
          ["Dallas", [100.0, 199.0], [100.0, 202.0]],
          ["Kansas City", [108.0, 209.0], [72.0, 208.0]],
          ["Houston", [102.0, 193.0], [102.0, 196.0]],
          ["Atlanta", [120.0, 200.0], [123.0, 201.0]],
          ["Los Angeles", [62.0, 200.0], [23.0, 198.0]],
          ["Seattle", [66.0, 226.0],[40.0, 227.0]],
          ["San Francisco", [58.0, 205.0],[17.0, 205.0]],
          ["Philadelphia", [140.0, 211.0],[143.0, 206.0]],
          ["Miami", [123.0, 185.0],[126.0, 185.0]],
          ["Boston", [148.0, 220.0], [151.0, 220.0]],
          ["Vancouver", [69.5, 233.0], [40.0, 235.0]],
          ["Monterrey", [86.0, 181.0],[86.0, 184.0]], 
          ["Toronto", [133.0, 220.0], [134.0, 226.0]],
          ["Guadalajara", [80.0, 170.0], [40.0, 168.0]]]
left_padding = 0
bottom_padding = 0
width = 595
height = 842
poule_width = 48
poule_height = 205
pouleland_height = 40
outsidearea = "#9e9e9e"
fifacolor = "#326295"
banpar = "#ff89a8"
banvis = "#ea9c00"
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
#mapversie = "Simple"
#mapversie = "Fifa"
#mapversie = "GB"
mapversie = "Russia"
colwidthgame = 72
pcol1 = HexColor("#9FA5D5")
pcol2 = HexColor("#E8F5C8")
ccol1 = HexColor("#9e9e9e")
ccol2 = HexColor("#b0b0b0")
lcol1 = HexColor("#849B5C")
lcol2 = HexColor("#BFFFC7")
rowheightgame = 18
gameline = 550
legendawidth = 75
legendarowheight = 10
legenda1x = 10
legenda1y = 5
legenda1l = 14
legenda2x = 210
legenda2y = 5
legenda2l = 12
legenda3x = 375
legenda3y = 5
legenda3l = 13
legenda4x = 150
legenda4y = 160
legenda4l = 3
legenda5x = 510
legenda5y = 120
legenda5l = 6

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
    if poule % 2 == 0:
        mode = "l"
    else:
        mode = "r"
    drawHorizontalRect(my_canvas, left_margin + poule * poule_width, poulerect_y, poule_width, poule_height, mode, pcol1, pcol2)

line = gameline
for j in range(13):
    if j == 9 or j == 11 or j == 12:
        line -= 10
    if j % 2 == 0:
        mode = "t"
    else:
        mode = "b"
    drawVerticalRect(my_canvas, left_margin, line - 3.5 - j * rowheightgame, 8 * colwidthgame, rowheightgame, mode, ccol1, ccol2)
    
drawHorizontalRect(my_canvas, legenda1x, legenda1y, legendawidth, legendarowheight * legenda1l, "l", lcol1, lcol2)
drawHorizontalRect(my_canvas, legenda2x, legenda2y, legendawidth, legendarowheight * legenda2l, "l", lcol1, lcol2)    
drawHorizontalRect(my_canvas, legenda3x, legenda3y, legendawidth, legendarowheight * legenda3l, "l", lcol1, lcol2)
drawHorizontalRect(my_canvas, legenda4x, legenda4y, legendawidth, legendarowheight * legenda4l, "l", lcol1, lcol2)
drawHorizontalRect(my_canvas, legenda5x, legenda5y, legendawidth, legendarowheight * legenda5l, "l", lcol1, lcol2)
    
teamcounter = 0
eteamcouner = 0
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
        if nationsdata[teamcounter][9] == "e":
            my_canvas.setFillColor(HexColor(colors[eteamcouner]))
            my_canvas.circle(float(nationsdata[teamcounter][6]), float(nationsdata[teamcounter][7]), 2.0, stroke = 0, fill = 1)
            eteamcouner += 1
        else:
            drawing = scaleSVG("Flags/" + nationsdata[teamcounter][8] + "tw.svg", 0.25)
            renderPDF.draw(drawing, my_canvas, float(nationsdata[teamcounter][6]), float(nationsdata[teamcounter][7]))
        pouleland_y = pouleland_y - (pouleland_height + poule_margin)
        teamcounter += 1
    poule_x = poule_x + poule_width
    
for i in range(len(cities)):
    my_canvas.setFillColor(HexColor(colors[i]))
    my_canvas.circle(float(cities[i][1][0]), float(cities[i][1][1]), 2.0, stroke = 0, fill = 1)
    my_canvas.setFillColor(HexColor("#ffffff"))
    my_canvas.setFont(socfont, 7)
    my_canvas.drawString(float(cities[i][2][0]), float(cities[i][2][1]), cities[i][0])
    
calindex = 0
limitcalindex = 103
gameindex = 0
categoryrectdy = 15
categorystrdy = 17
categoryrectheight = 9
 
for j in range(13):
    if j == 0:
        my_canvas.setFont(socfont, 8)
        my_canvas.setFillColor(HexColor(fifacolor))
        my_canvas.rect(left_margin, gameline + categoryrectdy, 8 * colwidthgame, categoryrectheight, stroke = 0, fill = 1)
        my_canvas.setFillColor(HexColor("#ffffff"))
        my_canvas.drawString(left_margin + 1.0, gameline + categorystrdy, "Group Stage")
        my_canvas.drawString(left_margin + 60.0, gameline + categorystrdy, "Host")
        my_canvas.setFillColor(HexColor(colors[13]))
        my_canvas.circle(left_margin + 80.0, gameline + categorystrdy + 3.5, 2.0, stroke = 0, fill = 1)
        my_canvas.setFillColor(HexColor("#ffffff"))
        my_canvas.drawString(left_margin + 90.0, gameline + categorystrdy, "A.M.")
        renderPDF.draw(scaleSVG("Clocks/halfmoontw.svg", 0.2), my_canvas, left_margin + 105.6, gameline + categorystrdy)
    for i in range(8):
        if calindex <= limitcalindex:
            if len(gameevents[calindex].summary) == 2:
                category = gameevents[calindex].summary[0]
            else:
                category = gameevents[calindex].summary[5]
            opponent1 = ""
            opponent2 = ""
        else:
            break
        drawing = scaleSVG("SVG/calendar-blank.svg", 0.42)
        renderPDF.draw(drawing, my_canvas, left_margin + i * colwidthgame, gameline - 2)
        my_canvas.setFont(socfont, 7)
        my_canvas.setFillColor(HexColor("#ffffff"))
        if category >= "A" and category <= "L":
            description = gameevents[calindex].description
            idx = description.find("-")
            opponent1 = description[:idx - 1]
            opponent2 = description[idx + 2:]
        if category == "3" or category == "1" or category == "Q" or category == "S" or category == "T" or category == "Z":
            my_canvas.drawString(left_margin + i * colwidthgame + 1.0, gameline + 7.5, gameevents[calindex].summary[1:4])
            description = gameevents[calindex].description
            idx = description.find("-")
            opponent1 = description[:idx - 1]
            opponent2 = description[idx + 2:]
        else:
            my_canvas.setFont(socfontbold, 7)
            my_canvas.setFillColor(HexColor("#ffffff"))
            my_canvas.drawString(left_margin + i * colwidthgame + 5.5, gameline + 8.0, category)
        my_canvas.setFont(socfont, 7)  
        my_canvas.setFillColor(HexColor("#000000"))
        daystr = str(gameevents[calindex].day)
        monthstr = str(gameevents[calindex].month)
        datestr = daystr + "-" + monthstr
        if len(daystr) == 1:
            my_canvas.drawString(left_margin + i * colwidthgame + 2.0, gameline + 0.5, datestr)
        else:
            my_canvas.drawString(left_margin + i * colwidthgame + 0.45, gameline + 0.5, datestr)
        my_canvas.drawString(left_margin + i * colwidthgame + 30, gameline, opponent2)
        my_canvas.drawString(left_margin + i * colwidthgame + 30, gameline + 6, opponent1)
        [hour, minute] = converttimetztolocalclock(gameevents[calindex].starttime)
        strhour = "{:02d}".format(hour)
        strminute = "{:02d}".format(minute)
        startevent = strhour + strminute
        drawing = scaleSVG("Clocks/" + startevent + "tw.svg", 0.4)
        renderPDF.draw(drawing, my_canvas, left_margin + i * colwidthgame + 15, gameline - 1.0)
        if hour < 12 and j < 9:
            renderPDF.draw(scaleSVG("Clocks/halfmoontw.svg", 0.2), my_canvas, left_margin + i * colwidthgame + 21.6, gameline - 1.0)
        locidx = lookuplocation(gameevents[calindex].location)
        my_canvas.setFillColor(HexColor(colors[locidx]))
        my_canvas.circle(left_margin + i * colwidthgame + 17.7, gameline + 0.15, 2.0, stroke = 0, fill = 1)
        calindex += 1
    gameline -= rowheightgame
    if j == 8:
        gameline -= 10
        my_canvas.setFillColor(HexColor(fifacolor))
        my_canvas.rect(left_margin, gameline + categoryrectdy, 8 * colwidthgame, categoryrectheight, stroke = 0, fill = 1)
        my_canvas.setFillColor(HexColor("#ffffff"))
        my_canvas.drawString(left_margin + 1.0, gameline + categorystrdy, "Round of 32")
    if j == 10:
        gameline -= 10
        my_canvas.setFillColor(HexColor(fifacolor))
        my_canvas.rect(left_margin, gameline + categoryrectdy, 8 * colwidthgame, categoryrectheight, stroke = 0, fill = 1)
        my_canvas.setFillColor(HexColor("#ffffff"))
        my_canvas.drawString(left_margin + 1.0, gameline + categorystrdy, "Round of 16")
    if j == 11:
        gameline -= 10
        my_canvas.setFillColor(HexColor(fifacolor))
        my_canvas.rect(left_margin, gameline + categoryrectdy, 4 * colwidthgame, categoryrectheight, stroke = 0, fill = 1)
        my_canvas.setFillColor(HexColor(fifacolor))
        my_canvas.rect(left_margin + 4 * colwidthgame, gameline + categoryrectdy, 2 * colwidthgame, categoryrectheight, stroke = 0, fill = 1)
        my_canvas.setFillColor(HexColor(fifacolor))
        my_canvas.rect(left_margin + 6 * colwidthgame, gameline + categoryrectdy, 1 * colwidthgame, categoryrectheight, stroke = 0, fill = 1)
        my_canvas.setFillColor(HexColor(fifacolor))
        my_canvas.rect(left_margin + 7 * colwidthgame, gameline + categoryrectdy, 1 * colwidthgame, categoryrectheight, stroke = 0, fill = 1)
        my_canvas.setFillColor(HexColor("#ffffff"))
        my_canvas.drawString(left_margin + 1.0, gameline + categorystrdy, "Quarter finals")
        my_canvas.drawString(left_margin + 4 * colwidthgame + 1.0, gameline + categorystrdy, "Semi finals")
        my_canvas.drawString(left_margin + 6 * colwidthgame + 1.0, gameline + categorystrdy, "Bronze final")
        my_canvas.drawString(left_margin + 7 * colwidthgame + 1.0, gameline + categorystrdy, "Final")    

teamcounter = 0
for i in range(16):
    drawing = scaleSVG("Logos/" + nationsdata[teamcounter][0] + ".svg", float(nationsdata[teamcounter][1]) / 4)
    renderPDF.draw(drawing, my_canvas, 10, 10 + teamcounter * 9)
    teamcounter += 1

my_canvas.save()
key = input("Wait")
