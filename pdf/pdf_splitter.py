from PyPDF2 import PdfWriter, PdfReader

inputpdf = PdfReader(open("D:\\OneDrive\\Desktop\\tax-forms.pdf", "rb"))

for i in range(len(inputpdf.pages)):
    output = PdfWriter()
    output.add_page(inputpdf.pages[i])
    with open("document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)
