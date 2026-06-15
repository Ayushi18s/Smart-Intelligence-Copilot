from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def generate_pdf(report_text):
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)

    y = 750

    for line in report_text.split("\n"):
        pdf.drawString(50, y, line[:100])
        y -= 20

        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()

    buffer.seek(0)

    return buffer.getvalue()