from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Frame, PageTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch,cm

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


pdfmetrics.registerFont(TTFont('Consola', r'C:\Windows\Fonts\consola.ttf'))
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-bd', r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Impact', r'C:\Windows\Fonts\impact.ttf'))

def create_pdf_with_custom_margins(output_path):
    story = []
    # 获取默认样式表
    styles = getSampleStyleSheet()

    # 定义两个不同的帧 (Frame)，分别对应两种不同的边距
    frame1 = Frame(0.5 * inch, 0.5 * inch, 7.5 * inch, 9.5 * inch, id='frame1')  # 边距较大
    frame2 = Frame(1 * inch, 1 * inch, 6.5 * inch, 8.5 * inch, id='frame2')  # 边距较小

    # 定义两个不同的页面模板 (PageTemplate)
    page_template1 = PageTemplate(id="first_page", frames=frame1, onPage=_add_header_footer_first)
    story.append(Paragraph("First page with big margin.", styles["Normal"]))
    # story.append(PageBreak())
    page_template2 = PageTemplate(id="other_pages", frames=frame2, onPage=_add_header_footer_other)
    story.append(Paragraph("Second page with small margin.", styles["Normal"]))

    # 将页面模板列表传入 DocTemplate
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    doc.addPageTemplates([page_template1, page_template2])

    # 添加一些内容到文档中
    # story = [
    #     Paragraph("First page with big margin.", styles["Normal"]),
    #     # PageBreak(),
    #     Paragraph("Second page with small margin.", styles["Normal"])
    # ]

    # 构建 PDF 文件
    doc.build(story,onFirstPage=page_template1,onLaterPages=page_template2)


# 自定义函数用于添加页眉和页脚（可选）
def _add_header_footer_first(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 16)
    canvas.drawString(inch, 10.5 * inch, "Initial page with big margin")  # 首页特定页眉
    canvas.restoreState()


def _add_header_footer_other(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 12)
    canvas.drawString(inch, 0.75 * inch, f"Page {doc.page}")  # 后续页面通用页脚
    canvas.restoreState()


create_pdf_with_custom_margins("custom_margins.pdf")