'''
Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1,
repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=None,
spaceAfter=None)

'''
'''
Table and Tablestyle
TableStyle user Methods
1.TableStyle(commandSequence)
The creation method initializes the TableStyle with the argument command sequence
eg:

     LIST_STYLE = TableStyle(
         [('LINEABOVE', (0,0), (-1,0), 2, colors.green),
         ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
         ('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),
         ('ALIGN', (1,1), (-1,-1), 'RIGHT')]

2. TableStyle.add(commandSequence)
This method allows you to add commands to an existing TableStyle, i.e. you can build up
TableStyles in multiple statements.
eg:
LIST_STYLE.add('BACKGROUND', (0,0), (-1,0), colors.Color(0,0.7,0.7))
3.TableStyle.getCommands()
This method returns the sequence of commands of the instance.
cmds = LIST_STYLE.getCommands()

4.TableStyle Commands
TableStyle Cell Formatting Commands

FONT - takes fontname, optional fontsize and optional leading.
FONTNAME (or FACE) - takes fontname.
FONTSIZE (or SIZE)- takes fontsize in points; leading may get out of sync.
LEADING- takes leading in points.
TEXTCOLOR- takes a color name or (R,G,B) tuple.
ALIGNMENT (or ALIGN)- takes one of LEFT, RIGHT and CENTRE (or CENTER) or DECIMAL.
LEFTPADDING- takes an integer, defaults to 6.
RIGHTPADDING- takes an integer, defaults to 6.
BOTTOMPADDING- takes an integer, defaults to 3.
TOPPADDING- takes an integer, defaults to 3.
BACKGROUND- takes a color defined by an object, string name or numeric tuple/list,
  or takes a list/tuple describing a desired gradient fill which should
  contain three elements of the form [DIRECTION, startColor, endColor]
  where DIRECTION is either VERTICAL or HORIZONTAL.
ROWBACKGROUNDS- takes a list of colors to be used cyclically.
COLBACKGROUNDS- takes a list of colors to be used cyclically.
VALIGN- takes one of TOP, MIDDLE or the default BOTTOM


TableStyle Line Commands
Line commands begin with the identifier, the start and stop cell coordinates and always follow this with the thickness 
(in points) and color of the desired lines. Colors can be names, or they can be specified as a (R, G, B) tuple, where
 R, G and B are floats and (0, 0, 0) is black. The line command names are: GRID, BOX, OUT- LINE, INNERGRID, LINEBELOW, 
 LINEABOVE, LINEBEFORE and LINEAFTER. BOX and OUTLINE are equivalent, and GRID is the equivalent of applying both BOX 
 and INNERGRID.

#TableStyle Span Commands
Our Table classes support the concept of spanning, but it isn't specified in the same way as html. The style
specification
       SPAN, (sc,sr), (ec,er)
indicates that the cells in columns sc - ec and rows sr - er should be combined into a super cell with con- tents
 determined by the cell (sc, sr). The other cells should be present, but should contain empty strings or you may 
 get unexpected results.

'''
# example
import subprocess
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('hei', 'SIMHEI.TTF'))
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
import time

elements = []

# TableStyle Commands
#  BACKGROUND, and TEXTCOLOR commands
data = [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t = Table(data, colWidths=[100, 100, 100, 100, 100])
t.setStyle(TableStyle([('BACKGROUND', (1, 1), (-2, -2), colors.green),    # (Identifier, start, stop, thickness, color)
                       ('TEXTCOLOR', (0, 0), (1, -1), colors.red)]))

elements.append(t)
#
data = [['\n']*5,
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t = Table(data, colWidths=[100, 100, 100, 100, 100],rowHeights=[15,30,30,30],hAlign='CENTER',vAlign="CENTER",                   #('LEFT', 'RIGHT', 'CENTER' or 'CENTRE')
          style=[('GRID', (0, 1), (-1, -1), 1, colors.black),
                 ('BOX', (1, 0), (1, -1), 2, colors.red),
                 ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                 ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                 ])

elements.append(t)

#
data = [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t = Table(data, 5 * [0.4 * inch], 4 * [0.4 * inch])
t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                       ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                       ('VALIGN', (0, 0), (0, -1), 'TOP'),
                       ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                       ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                       ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                       ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                       ]))

elements.append(t)
# print(elements)

# TableStyle Line Commands

data = [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t = Table(data, style=[('GRID', (1, 1), (-2, -2), 1, colors.green),
                       ('BOX', (0, 0), (1, -1), 2, colors.red),
                       ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                       ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                       ])

elements.append(t)
#
data = [['00', '01', '闪电', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t = Table(data, style=[
    ('FONTNAME', (0, 0), (-1, -1), 'hei'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('GRID', (1, 1), (-2, -2), 1, colors.green),
    ('BOX', (0, 0), (1, -1), 2, colors.red),
    ('BOX', (0, 0), (-1, -1), 2, colors.black),
    ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
    ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
    ('BACKGROUND', (0, 0), (0, 1), colors.pink),
    ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
    ('BACKGROUND', (2, 2), (2, 3), colors.orange),
])

elements.append(t)

# TableStyle Span Commands

data = [['Top\nLeft', '', '02', '03', '04'],
        ['', '', '12', '13', '14'],
        ['20', '21', '22', 'Bottom\nRight', ''],
        ['30', '31', '32', '', '']]
T = Table(data, style=[
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('BACKGROUND', (0, 0), (1, 1), colors.palegreen),
    ('SPAN', (0, 0), (1, 1)),
    ('BACKGROUND', (-2, -2), (-1, -1), colors.pink),
    ('SPAN', (-2, -2), (-1, -1)),
])

# print(elements)
doc = SimpleDocTemplate('demo5.pdf')
doc.build(elements)

time.sleep(0.5)
path = r"C:\Program Files\Tracker Software\PDF Editor\PDFXEdit.exe C:\work\git\Report_Automatically\demo5.pdf"
subprocess.Popen(path)