import os
from PyPDF2 import PdfReader, PdfWriter
from format_text import examinar_texto

def split_pages(input_path, output_folder, pages):
   
    pages_to_extract = examinar_texto(pages)
    print(pages_to_extract)
    
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

        print(f'Páginas del PDF divididas con éxito. Archivos guardados en: {output_folder}')

    except Exception as e:
        print(f'Error al dividir el PDF: {e}')



#Ejemplo de uso

hojas = '1,2,10+12,13-15,' # Lista de páginas a extraer
input = 'book/book.pdf'  # Reemplaza con la ruta de tu archivo PDF de entrada
output = 'book/probe'  # Reemplaza con la carpeta de salida que desees


split_pages(input, output, hojas)
