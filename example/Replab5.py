#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.setStrokeColor(Color(0, 0, 0, alpha=0.5))
        self.line(10*mm, 15*mm, A4[0] - 10*mm, 15*mm)
        self.setFillColor(Color(0, 0, 0, alpha=0.5))
        self.drawCentredString(A4[0]/2, 10*mm, "Page %d of %d" % (self._pageNumber, page_count))
 
def main(filename):
    pdfmetrics.registerFont(TTFont('微软雅黑', 'msyh.ttf'))
    
    title = ParagraphStyle(name = 'Title',
        fontName = '微软雅黑',
        fontSize = 22,
        leading = 16,
        alignment = 1,
        spaceAfter = 20)

    image = Image("images/title.jpg")
    image.drawWidth = 160
    image.drawHeight = 160*(image.imageHeight/image.imageWidth)
    elements = [
        Paragraph('继承Canvas', title),
        Paragraph("Hello"),
        image,
        PageBreak(),
        Paragraph("world"),
    ]
    doc = SimpleDocTemplate(filename)
    doc.build(elements, canvasmaker=NumberedCanvas)
    
    
if __name__ == "__main__":
    main("Replab5.pdf")
    