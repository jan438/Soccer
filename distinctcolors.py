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
import numpy as np

colors = [
"#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438","#A8A202","#158FAD","#14AAF5","#CD0027",
"#4073FF","#D38895","#884DFF","#AF38EB","#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438",
"#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438","#A8A202","#158FAD","#14AAF5","#CD0027",
"#4073FF","#D38895","#884DFF","#AF38EB","#88255F","#DB4035","#FF9933","#FAD000","#AFB83B","#7ECC49","#E7E84F","#299438",
          ]
if sys.platform[0] == 'l':
    path = '/home/jan/git/Soccer'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Soccer"
os.chdir(path)
my_canvas = canvas.Canvas("PDF/distinctcolors.pdf")
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
