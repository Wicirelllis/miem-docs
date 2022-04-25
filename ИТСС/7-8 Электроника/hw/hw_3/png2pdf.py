import PyPDF2
from PyPDF2 import PdfFileMerger, PdfFileReader
import img2pdf

INPUT_PDF = "hw_3.pdf"
INPUT_IMG = "layout.png"

# convert png to pdf
with open("img.pdf","wb") as f:
    f.write(img2pdf.convert(INPUT_IMG))

# scale img-pdf to proper width
pdf = PyPDF2.PdfFileReader(INPUT_PDF, "rb")
page_width = pdf.getPage(0).mediaBox.getWidth()

img = PdfFileReader("img.pdf").getPage(0)
img.scaleBy(float(page_width / img.mediaBox.getWidth()))

writer = PyPDF2.PdfFileWriter()
writer.addPage(img)
with open("img_scaled.pdf", "wb+") as f:
    writer.write(f)

# concat in one file
merger = PdfFileMerger()
merger.append("hw_3.pdf")
merger.append("img_scaled.pdf")
merger.write("hw_3_with_img.pdf")
merger.close()
