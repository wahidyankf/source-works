import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_test_pdf(filename, text):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Add some test content
    c.setFont("Helvetica", 24)
    c.drawString(100, height - 100, text)

    c.save()


# Create test PDFs
test_dir = "test-data"
os.makedirs(test_dir, exist_ok=True)

create_test_pdf(os.path.join(test_dir, "document1.pdf"), "This is Document 1")
create_test_pdf(os.path.join(test_dir, "document2.pdf"), "This is Document 2")
create_test_pdf(os.path.join(test_dir, "document3.pdf"), "This is Document 3")
