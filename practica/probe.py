import fitz  # Importa la librería PyMuPDF

pdf_file = "book/book.pdf"
doc = fitz.open(pdf_file)

# Páginas que deseas separar (por ejemplo, 1, 2 y 3)
pages_to_extract = [0, 1, 2]

for page_num in pages_to_extract:
    page = doc[page_num]
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    new_doc.save(f"pagina_{page_num + 1}.pdf")
    new_doc.close()

doc.close()
