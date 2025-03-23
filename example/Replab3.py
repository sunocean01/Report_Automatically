#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm


class MyDocTemplate(BaseDocTemplate):
    
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [Frame(2.5*cm, 2.5*cm, 15*cm, 25*cm, id='F1')])
        self.addPageTemplates(template)
        self.chapter = 0
        self.section = 0

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Title':
                self.chapter += 1
                self.canv.bookmarkPage(f"chapter{self.chapter}")
                self.canv.addOutlineEntry(f"Chapter {self.chapter}", f"chapter{self.chapter}", level=0)
            elif style == 'Heading1':
                self.section += 1
                self.canv.bookmarkPage(f"section{self.section}")
                self.canv.addOutlineEntry(f"Section {self.section}", f"section{self.section}", level=1)

def main(filename):
    pdfmetrics.registerFont(TTFont('微软雅黑', 'msyh.ttf'))
    
    title = ParagraphStyle(name = 'Title',
        fontName = '微软雅黑',
        fontSize = 22,
        leading = 16,
        alignment = 1,
        spaceAfter = 20)

    h1 = ParagraphStyle(
        name = 'Heading1',
        fontSize = 14,
        leading = 16)

    story = []
    
    story.append(Paragraph('继承BaseDocTemplate', title))
    story.append(Paragraph('Section 1', h1))
    story.append(Paragraph('Text in Section 1.1'))
    story.append(PageBreak())
    story.append(Paragraph('Section 2', h1))
    story.append(Paragraph('Text in Section 1.2'))
    story.append(PageBreak())
    story.append(Paragraph('Chapter 2', title))
    story.append(Paragraph('Section 1', h1))
    story.append(Paragraph('Text in Section 2.1'))

    doc = MyDocTemplate(filename)
    doc.build(story)


if __name__ == '__main__':
    main("Replab3.pdf")
    
