# example
import time
import subprocess

from reportlab.lib.units import inch,cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from reportlab.lib.pagesizes import A4

# pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from django.http import HttpResponse
# from io.cStringIO import StringIO   #Python2 适用
from io import StringIO
from reportlab import rl_config
from reportlab.lib.utils import simpleSplit
from reportlab.lib.fonts import addMapping



from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib import pagesizes, colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.graphics.shapes import Drawing, Rect
from reportlab.platypus import Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageTemplate
from reportlab.platypus.frames import Frame

from functools import partial



# 注册字体，或者把windows文件夹里的字体拷贝到reportLab的字体文件夹里,理论上可行；
pdfmetrics.registerFont(TTFont('Consola', r'C:\Windows\Fonts\consola.ttf'))
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Impact', r'C:\Windows\Fonts\impact.ttf'))

pdf_name = r"TemplateSample.pdf"
PAGESIZE = pagesizes.portrait(pagesizes.A4)
doc = SimpleDocTemplate(pdf_name, pagesize=PAGESIZE,
                        leftMargin=2.2*cm,
                        rightMargin=2.2*cm,
                        topMargin=0.5*cm,
                        bottomMargin=2.5*cm)

# doc = SimpleDocTemplate(pdf_name)

content = []
def hello_pdf(request):
    rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(TTFont('song', '/home/yisl04/.fonts/simsun.ttc'))
    pdfmetrics.registerFont(TTFont('fs', '/home/yisl04/.fonts/simfang.ttf'))
    pdfmetrics.registerFont(TTFont('hei', '/home/yisl04/.fonts/simhei.ttf'))
    pdfmetrics.registerFont(TTFont('yh', '/home/yisl04/.fonts/msyh.ttf'))

    # 设置字体：常规、斜体、粗体、粗斜体
    addMapping('cjk', 0, 0, 'song')  # normal
    addMapping('cjk', 0, 1, 'fs')  # italic
    addMapping('cjk', 1, 0, 'hei')  # bold
    addMapping('cjk', 1, 1, 'yh')  # italic and bold

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'

    temp = StringIO()
    p = canvas.Canvas(temp)

    # 默认(0, 0)点在左下角，此处把原点(0,0)向上和向右移动，后面的尺寸都是相对与此原点设置的
    # 注意：移动原点时，向右向上为正，坐标系也是向右为+x，向上为+y
    p.translate(0.5 * inch, 0.5 * inch)
    # 设置字体
    p.setFont('song', 16)
    # 设置颜色，画笔色和填充色
    p.setStrokeColorRGB(0.2, 0.5, 0.3)
    p.setFillColorRGB(1, 0, 1)
    # 画一个矩形
    p.rect(0, 0, 3 * inch, 3 * inch, fill=1)
    # 旋转文字方向
    p.rotate(90)
    p.setFillColorRGB(0, 0, 0.77)
    p.drawString(3 * inch, -3 * inch, u"我是吴仁智，呵呵！")
    p.rotate(-90)
    p.setFont('yh', 16)
    p.drawString(0, 0, u"drawString默认不换行！")
    # 插入图片
    p.drawImage("/home/yisl04/public_html/yisl04.png", 5 * inch, 5 * inch, inch, inch)
    # 设置drawString最大宽度
    L = simpleSplit(u'simpleSplit 只能用于 drawString 英文断行。', 'yh', 16, 9 * inch)
    y = 9 * inch
    for t in L:
        p.drawString(0, y, t)
        y -= p._leading

    # Paragraph下中文断行(网上摘抄)
    def wrap(self, availWidth, availHeight):
        # work out widths array for breaking
        self.width = availWidth
        leftIndent = self.style.leftIndent
        first_line_width = availWidth - (leftIndent + self.style.firstLineIndent) - self.style.rightIndent
        later_widths = availWidth - leftIndent - self.style.rightIndent
        try:
            self.blPara = self.breakLinesCJK([first_line_width, later_widths])
        except:
            self.blPara = self.breakLines([first_line_width, later_widths])
        self.height = len(self.blPara.lines) * self.style.leading
        return (self.width, self.height)

    Paragraph.wrap = wrap

    # 中文断行还可以使用下面这种简单的方法
    # from reportlab.lib.styles import ParagraphStyle
    # ParagraphStyle.defaults['wordWrap']="CJK"

    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']
    style.fontName = 'song'
    style.fontSize = 16
    # 设置行距
    style.leading = 20
    # 首行缩进
    style.firstLineIndent = 32
    Pa = Paragraph(
        u'<b>这里是粗体</b>，<i>这里是斜体</i>, <strike>这是删除线</strike>, <u>这是下划线</u>, <sup>这是上标</sup>, <em>这里是强调</em>, <font color=#ff0000>这是红色</font>',
        style)

    Pa.wrapOn(p, 6 * inch, 8 * inch)
    Pa.drawOn(p, 0, 5 * inch)

    p.showPage()
    p.save()
    response.write(temp.getvalue())
    return response


def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
    canvas.restoreState()

def footer(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.bottomMargin)
    content.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()

def header_and_footer(canvas, doc, header_content, footer_content):
    header(canvas, doc, header_content)
    footer(canvas, doc, footer_content)

styles = getSampleStyleSheet()
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
header_content = Paragraph("This is a header. testing testing testing  ", styles['Normal'])
footer_content = Paragraph("This is a footer. It goes on every page.  ", styles['Normal'])
template = PageTemplate(id='test', frames=frame, onPage=partial(header_and_footer, header_content=header_content, footer_content=footer_content))

doc.addPageTemplates([template])

doc.build([Paragraph("This is content")])



exit()
def page_layout(canvas, doc):
    # c = canvas("testoutput\Hello.pdf", pagesize='A4', bottomup=2, encodings='UTF8')
    image_log = 'log.jpg'
    image_slogan = 'slogan.jpg'
    # image.show()
    canvas.drawImage(image_log, 20, 750, width=60, height=65)
    canvas.drawImage(image_slogan, 400, 700, width=90, height=70)
    # canvas.setFont('Times-Roman', 10)

    page_num = canvas.getPageNumber()
    canvas.drawString(500, 15, f"Page:{page_num}")



p_style = getSampleStyleSheet()['Normal']      #取对应的功能
p_style_heading1 = getSampleStyleSheet()['Heading1']
p_style.fontName = 'Arial'
# p_style.fontName = 'Consola'
# p_style.fontName = 'Impact'
p_style.leading = 15         #行距
p_style.fontSize = 12
p_style.textColor = colors.black
p_style.alignment = 0      #0:左对齐； 1:居中； 2:右对齐
p_style.wordWrap = 'CJK'
par_style1 = ParagraphStyle(name='p_style1',
                            parent=p_style,    #继承父类
                            fontName='Arial',
                            fontSize = 22,
                            textColor = (0,0,153),
                            wordWrap = 'LTR',
                            spaceAfter=10, spaceBefore=10,)
par1 = Paragraph('HARVESTEC SERVICE CO., LTD',p_style_heading1)
content.append(par1)
content.append(Spacer(1,10))

par_style2 = ParagraphStyle(name='p_style2',
                            parent=p_style,
                            # fontName='SimSun',
                            fontSize=12,
                            textColor=(0, 0, 0),
                            wordWrap='LTR',
                            spaceAfter=10,
                            spaceBefore=10,
                            )
par2 = Paragraph('''Address:    Rm403,No.268 Xuanzhong Rd,Nanhui Industrial Zone. Shanghai 201300, China''',p_style)
content.append(par2)

par_style3 = ParagraphStyle(name='p_style2',
                            parent=p_style,
                            # fontName='SimSun',
                            fontSize=12,
                            textColor=(0, 0, 0),
                            wordWrap='LTR',
                            spaceAfter=0,
                            spaceBefore=5,
                            )
par3 = Paragraph("Mob:  +86 - 15951255485  13524569142",p_style)
content.append(par3)

par4 = Paragraph("E-mail:   info@harvestec.net",p_style)
content.append(par4)


doc.build(content, onFirstPage=page_layout, onLaterPages=page_layout)


time.sleep(0.5)
path = r"C:\Program Files\Tracker Software\PDF Editor\PDFXEdit.exe C:\work\git\Report_Automatically\TemplateSample.pdf"
subprocess.Popen(path)
