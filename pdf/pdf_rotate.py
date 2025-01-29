import PyPDF2

def rotate_pdf(input_pdf, output_pdf, rotation_angle):
    with open(input_pdf, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page.rotate(rotation_angle)
            pdf_writer.add_page(page)

        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)

if __name__ == '__main__':
    rotate_pdf("D:\\OneDrive\\Documents\\Misc\\input.pdf", "D:\\OneDrive\\Documents\\Misc\\output.pdf", 90)
