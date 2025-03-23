import datetime
import time
import subprocess


# pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from django.http import HttpResponse
# from io.cStringIO import StringIO   #Python2 适用
from io import StringIO

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


from reportlab import rl_config
from reportlab.lib import pagesizes, colors
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch,cm
from reportlab.lib.utils import simpleSplit

from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

from reportlab.graphics.shapes import Drawing, Rect

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageTemplate, Frame, PageBreak

from functools import partial



# 注册字体，或者把windows文件夹里的字体拷贝到reportLab的字体文件夹里,理论上可行；
pdfmetrics.registerFont(TTFont('Consola', r'C:\Windows\Fonts\consola.ttf'))
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-bd', r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Impact', r'C:\Windows\Fonts\impact.ttf'))

# C:\Windows\Fonts\arial.ttf
# C:\Windows\Fonts\arialbd.ttf
# C:\Windows\Fonts\arialbi.ttf
# C:\Windows\Fonts\ariali.ttf
# C:\Windows\Fonts\ARIALN.TTF
# C:\Windows\Fonts\ARIALNB.TTF
# C:\Windows\Fonts\ARIALNBI.TTF
# C:\Windows\Fonts\ARIALNI.TTF
# C:\Windows\Fonts\ariblk.ttf


def header(canvas, doc):
    styles = styles = getSampleStyleSheet()['Normal']
    header_style = ParagraphStyle(name='headerStyle',
                                  parent=styles,  # 继承父类
                                  fontName='Arial',
                                  fontSize=16,
                                  textColor=(0, 0, 153),
                                  wordWrap='LTR',
                                  spaceAfter=10, spaceBefore=10, )
    canvas.saveState()

    title_1 = Paragraph("HARVESTEC SERVICE CO., LTD", header_style)
    w, h = title_1.wrap(doc.width, doc.topMargin)
    title_1.drawOn(canvas,
                   # doc.leftMargin,
                   # doc.height + doc.topMargin - h
                   90,
                   810
                   )

    title_2 = Paragraph("Address:   Rm403, No.268 Xuanzhong Rd, Nanhui Industrial Zone. Shanghai 201300, China", styles)
    w, h = title_2.wrap(300, doc.topMargin)
    title_2.drawOn(canvas, 90, 775)

    title_3 = Paragraph("Mob: +86 - 15951255485   13524569142", styles)
    w, h = title_3.wrap(300, doc.topMargin)
    title_3.drawOn(canvas, 90, 760)

    title_4 = Paragraph("E-mail:    info@harvestec.net", styles)
    w, h = title_4.wrap(300, doc.topMargin)
    title_4.drawOn(canvas, 90, 748)

    canvas.restoreState()
    image_log = 'log.jpg'
    image_slogan = 'slogan.jpg'
    # image.show()
    canvas.drawImage(image_log, 20, 750, width=60, height=65)
    canvas.drawImage(image_slogan, 380, 750, width=90, height=70)
def myHeader(doc,styles):
    def header(canvas, doc,styles):

        header_style = ParagraphStyle(name='headerStyle',
                                      parent=styles,  # 继承父类
                                      fontName='Arial',
                                      fontSize=16,
                                      textColor=(0, 0, 153),
                                      wordWrap='LTR',
                                      spaceAfter=10, spaceBefore=10, )
        canvas.saveState()

        title_1 = Paragraph("HARVESTEC SERVICE CO., LTD", header_style)
        w, h = title_1.wrap(doc.width, doc.topMargin)
        title_1.drawOn(canvas,
                       # doc.leftMargin,
                       # doc.height + doc.topMargin - h
                       90,
                       810
                       )

        title_2 = Paragraph("Address:   Rm403, No.268 Xuanzhong Rd, Nanhui Industrial Zone. Shanghai 201300, China", styles)
        w, h = title_2.wrap(300, doc.topMargin)
        title_2.drawOn(canvas,90,775)

        title_3 = Paragraph("Mob: +86 - 15951255485   13524569142", styles)
        w, h = title_3.wrap(300, doc.topMargin)
        title_3.drawOn(canvas,90,760)

        title_4 = Paragraph("E-mail:    info@harvestec.net", styles)
        w, h = title_4.wrap(300, doc.topMargin)
        title_4.drawOn(canvas,90,748)

        canvas.restoreState()
        image_log = 'log.jpg'
        image_slogan = 'slogan.jpg'
        # image.show()
        canvas.drawImage(image_log, 20, 750, width=60, height=65)
        canvas.drawImage(image_slogan, 380, 750, width=90, height=70)

        # canvas.drawString(40, 750,'HARVESTEC SERVICE CO., LTD')
    def footer(canvas, doc,styles):
        canvas.saveState()
        footer_content = Paragraph("HARVESTEC SERVICE CO., LTD", styles)
        w, h = footer_content.wrap(doc.width, doc.bottomMargin)
        footer_content.drawOn(canvas, doc.leftMargin, h)

        page_num = canvas.getPageNumber()
        canvas.drawString(500, 15, f"Page:{page_num}")
        canvas.restoreState()
    def header_and_footer(canvas, doc,styles):
        header(canvas, doc,styles)
        footer(canvas, doc,styles)


    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='Header', frames=frame, onPage=partial(header_and_footer,styles=styles))

    doc.addPageTemplates([template])
def title(doc, styles):
    Title_01_style = ParagraphStyle(name='Title_01',
                                    parent=styles,  # 继承父类
                                    fontName='Arial-bd',
                                    fontSize=48,
                                    textColor=(0, 0, 0),
                                    wordWrap='LTR',
                                    alignment=1,
                                    spaceAfter=10, spaceBefore=10,
                                    )
    Title_01 = Paragraph("Certificate", style=Title_01_style)
    content.append(Title_01)

    Title_02_style = ParagraphStyle(name='Title_02',
                                    parent=styles,  # 继承父类
                                    fontName='Arial-bd',
                                    fontSize=28,
                                    textColor=(0, 0, 0),
                                    wordWrap='LTR',
                                    alignment=1,
                                    spaceAfter=10, spaceBefore=10,
                                    )
    content.append(Spacer(10, 25))

    Title_02 = Paragraph("Of Inspection", style=Title_02_style)
    Title_02.wrap(doc.width, doc.topMargin)
    content.append(Title_02)

def basicinfo_table():
    data = datetime.datetime.now().strftime("%d/%m/%Y")
    ShipName = "GENJI"
    IMO = 9289738
    Flag = 'GABONESE REPUBLIC'
    Station = "HARVESTEC"
    Loc = 'SHANGHAI'
    Class = 'RINA'
    CertNumb = 'HT20250301-001'
    data = [['Data:','ShipName/Unit:', 'IMO No.:', 'Flag:'],
            [f'{data}', f'{ShipName}', f'{IMO}', f'{Flag}'],
            ['Service Station:', 'Service Loc.:', 'Class Society:','Certificate No.'],
            [f'{Station}', f'{Loc}', f'{Class}', f'{CertNumb}'],
            ]
    t = Table(data, colWidths=[120,150,120,150],rowHeights=[20,20,20,20])
    t.setStyle(TableStyle([('BOX', (0, 0), (0, 1), 1, colors.black),
                           ('BOX', (1, 0), (1, 1), 1, colors.black),
                           ('BOX', (2, 0), (2, 1), 1, colors.black),
                           ('BOX', (3, 0), (3, 1), 1, colors.black),
                           ('BOX', (0, 2), (0, 3), 1, colors.black),
                           ('BOX', (1, 2), (1, 3), 1, colors.black),
                           ('BOX', (2, 2), (2, 3), 1, colors.black),
                           ('FONT', (0, 0), (-1, -1), "Arial"),         #整体字体
                           ('FONTSIZE', (0, 0), (-1, -1), 12),          #整体字体
                           ('FONT', (0, 0), (-1, 0), "Arial-bd"),       #标题字体
                           ('FONTSIZE', (0, 0), (-1, 0), 14),           #标题大小
                           ('FONT', (0, 2), (-1, 2), "Arial-bd"),
                           ('FONTSIZE', (0, 2), (-1, 2), 14),

                           ('VALIGN', (0, 0), (-1, -1), 'TOP',),         #整体
                           # ('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
                           # ('ALIGNMENT', (0, 1), (-1, 1), 'RIGHT'),
                           # ('ALIGNMENT', (0, 3), (-1, 3), 'RIGHT'),

                           ('BOX', (0, 0), (-1, -1), 2,colors.black),

                           ]
                          )
               )

    content.append(t)



if __name__ == "__main__":
    pdf_name = r"TemplateSample.pdf"
    PAGESIZE = pagesizes.portrait(pagesizes.A4)
    doc = SimpleDocTemplate(pdf_name, pagesize=PAGESIZE,
                            leftMargin=2.2 * cm,
                            rightMargin=2.2 * cm,
                            topMargin=3.5 * cm,
                            bottomMargin=2.5 * cm)
    styles = getSampleStyleSheet()['Normal']
    # myHeader(doc,styles)

    content = []

    title(doc, styles)
    content.append(Spacer(10,25))
    basicinfo_table()


    content.append(PageBreak())

    Tmp = Paragraph("Temporary Content", style=styles)
    content.append(Tmp)
    doc.build(content, onFirstPage=header, onLaterPages=header)
    time.sleep(0.5)
    path = r"C:\Program Files\Tracker Software\PDF Editor\PDFXEdit.exe C:\work\git\Report_Automatically\TemplateSample.pdf"
    subprocess.Popen(path)