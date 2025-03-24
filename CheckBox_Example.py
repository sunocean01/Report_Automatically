from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets.grids import Table, TableStyle, CellStyle
from reportlab.graphics.widgets.markers import CheckBox
from reportlab.platypus import Table


def create_checkbox():
    drawing = Drawing(400, 200)
    cb = CheckBox(10, 10, size=10, checked=True)
    drawing.add(cb)
    return drawing


# 创建PDF文档
c = canvas.Canvas("checkbox_example.pdf", pagesize=letter)
drawing = create_checkbox()
c.drawInline(drawing, 100, 750, preserveTransform=True)  # 位置调整以适应页面
c.save()