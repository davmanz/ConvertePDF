import os
from PyPDF2 import PdfReader, PdfWriter

def proc_text(txt):
    txt2 = txt.split(',')
    ar = []
    ar_format = []

    for i in range(len(txt2)):
        if len(txt2[i].split("-")) > 1:
            ar_format.append("range")
            ar.append([int(s) for s in txt2[i].split("-")])
        elif len(txt2[i].split("+")) > 1:
            ar_format.append("join")
            ar.append(tuple([int(s) for s in txt2[i].split("+")]))
        else:
            ar_format.append("numeric")
            ar.append(int(txt2[i]))

    return ar

def split_pages(input_path, output_folder, pages):

    print(input_path)
   
    pages_to_extract = proc_text(pages)
    
    try:
        # Abre el archivo PDF de entrada con PdfReader
        pdf_reader = PdfReader(input_path)

        # Crea la carpeta de salida si no existe
        os.makedirs(output_folder, exist_ok=True)

        for page_range in pages_to_extract:

            if isinstance(page_range, int):
                # Si se proporciona un número entero, extraer una página individual
                page_num = page_range
                if 0 < page_num <= len(pdf_reader.pages):
                    pdf_writer = PdfWriter()
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])

                    output_file_path = os.path.join(output_folder, f'pagina_{page_num}.pdf')
                    with open(output_file_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                else:
                    print(f'Página {page_num} fuera de rango, se omitirá.')

            elif isinstance(page_range, tuple):
                # Si se proporciona una tupla con dos números, extraer un rango de páginas
                start_page, end_page = page_range
                if 0 < start_page <= end_page <= len(pdf_reader.pages):
                    pdf_writer = PdfWriter()
                    for page_num in range(start_page, end_page + 1):
                        pdf_writer.add_page(pdf_reader.pages[page_num - 1])

                    output_file_path = os.path.join(output_folder, f'paginas_{start_page}-{end_page}.pdf')
                    with open(output_file_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                else:
                    print(f'Rango de páginas {start_page}-{end_page} fuera de rango, se omitirá.')

            elif isinstance(page_range, list):
                # Si se proporciona una lista [inicio, fin], extraer todas las páginas desde inicio hasta fin de forma individual
                for page_num in range(page_range[0], page_range[1] + 1):
                    if 0 < page_num <= len(pdf_reader.pages):
                        pdf_writer = PdfWriter()
                        pdf_writer.add_page(pdf_reader.pages[page_num - 1])

                        output_file_path = os.path.join(output_folder, f'pagina_{page_num}.pdf')
                        with open(output_file_path, 'wb') as output_file:
                            pdf_writer.write(output_file)
                    else:
                        print(f'Página {page_num} fuera de rango, se omitirá.')

            else:
                print(f'Formato de página no válido, se omitirá: {page_range}')

    except Exception as e:
        print(f'Error al dividir el PDF: {e}')