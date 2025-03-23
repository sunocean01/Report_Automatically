#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import  colors
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate, Image


def draw_text(st, text: str):
    return Paragraph(text, st)
 
 
def draw_img(path):
    img = Image(path)       # 读取指定路径下的图片
    img.drawWidth = 5*cm    # 设置图片的宽度
    img.drawHeight = 4*cm   # 设置图片的高度
    return img


def main(filename):
    pdfmetrics.registerFont(TTFont('微软雅黑', 'msyh.ttf'))
    
    style = getSampleStyleSheet()
    
    ts = style['Heading1']
    ts.fontName = '微软雅黑'    # 字体名
    ts.fontSize = 18        # 字体大小
    ts.leading = 30         # 行间距
    ts.alignment = 1        # 居中
    ts.bold = True
    
    hs = style['Heading2']
    hs.fontName = '微软雅黑'    # 字体名
    hs.fontSize = 15        # 字体大小
    hs.leading = 20         # 行间距
    hs.textColor = colors.red  # 字体颜色
    
    ns = style['Normal']
    ns.fontName = '微软雅黑'
    ns.fontSize = 12
    ns.wordWrap = 'CJK'     # 设置自动换行
    ns.alignment = 0        # 左对齐
    ns.firstLineIndent = 32 # 第一行开头空格
    ns.leading = 20
    
    doc = BaseDocTemplate(filename, showBoundary=0, pagesize=A4)

    frameT = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    
    w = doc.width / 3
    h = w
    bm = doc.height - h
    frame1 = Frame(doc.leftMargin, bm, w, h, id='col1')
    frame2 = Frame(doc.leftMargin + w, bm, doc.width-w, h, id='col2')
    frame3 = Frame(doc.leftMargin, doc.bottomMargin, doc.width , bm-doc.topMargin, id='col3')
    
    doc.addPageTemplates([
        PageTemplate(id='TwoCol', frames=[frame1, frame2, frame3]),
        PageTemplate(id='OneCol', frames=frameT),
    ])
    
    
    elements = []
    
    
    elements.append(draw_img("images/title.jpg"))
    elements.append(draw_text(ns, ' 《超级马里奥兄弟》于1985年9月13日发售，这是一款任天堂针对FC主机全力度身订造的游戏，被称为TV游戏奠基之作。这个游戏被赞誉为电子游戏的原始范本，确立了角色、游戏目的、流程分布、操作性、隐藏要素、BOSS、杂兵等以后通用至今的制作概念。《超级马里奥兄弟》成为游戏史首部真正意义上的超大作游戏，游戏日本本土销量总计681万份，海外累计更是达到了3342万份的天文数字。'))
    elements.append(NextPageTemplate('OneCol'))
    elements.append(PageBreak())
    elements.append(draw_text(ns,"Frame one column, "))
    
    doc.build(elements)



if __name__ == '__main__':
    main("Replab2.pdf")
    