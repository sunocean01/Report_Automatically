
import reportlab.pdfgen as gen
from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas
import reportlab.graphics as gh
import reportlab.lib as lb
import reportlab.pdfbase as bs
import reportlab.platypus as pp
from PIL import Image
from reportlab.platypus import Paragraph


from reportlab.graphics import shapes

# for library in [gen,gh,lb,bs,pp]:
#     print("pdfgen methods:")
#     for i in [s for s in dir(library) if not s.startswith("_")]:
#         print(i)
#     print("*"*50)


# shp = gh.shapes.getRectsBounds([[100,200,150,200],[50,200,70,80]])
# print(shp)


c = canvas.Canvas("testoutput\Hello.pdf",pagesize='A4',bottomup=2,encodings='UTF8')
image_log = 'log.jpg'
image_slogan = 'slogan.jpg'
# image.show()
c.drawImage(image_log,30,700,width=60,height=65)
c.drawImage(image_slogan,400,700,width=90,height=70)


txt = '''Rm 403, No.268 Xuanzhong Rd, Nanhui Industrial Zone.      Shanghai 201300, China
  Mob: +86 - 15951255485
 E-mail:info@harvestec.net
'''

Paragraph(txt)

c.setAuthor("HARVESTEC")
c.setTitle("Certificate")

# c.drawString(200,700,"DrawString",)
# c.drawRightString(200,600,"DrawRightString")
# c.drawCentredString(200,500,"DrawCenterString")
# c.drawString(200,700,"Hello PDF! \n No. 2356847",)
# image = Image.open('log.gif')


c.showPage()
c.save()

