from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.lib.units import mm,cm
import qrcode
from reportlab.pdfgen import canvas
def create_qr_code(data, filename="qr_image.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

def add_qr_to_pdf(qr_filename, pdf_filename="output_with_qr.pdf"):
    c = canvas.Canvas(pdf_filename)
    c.drawString(100, 750, "This is a sample document with an embedded QR Code.")  # Add text to the PDF

    # Inserting the QR image into the PDF at position (x=150, y=650), maintaining its size.
    c.drawImage(qr_filename, 150, 650, width=120, height=120)

    c.save()

if __name__ == "__main__":
    data_for_qr = "https://www.example.com"
    qr_image_file = "example_qr.png"
    output_pdf_file = "document_with_qr.pdf"

    create_qr_code(data=data_for_qr, filename=qr_image_file)  # Generate QR code as PNG file
    add_qr_to_pdf(qr_image_file, pdf_filename=output_pdf_file)  # Embed it into a PDF

