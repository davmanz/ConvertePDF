from time import sleep
from pdf2docx import Converter
from pdf2docx import parse
from flet import (app,
                  Page, 
                  Row, 
                  TextField, 
                  icons, 
                  ElevatedButton, 
                  FilePickerResultEvent, 
                  FilePicker,
                  ProgressBar)

def main(page:Page):
    page.title = "Conversor PDF a DOCX"
    page.vertical_alignment = 'center'
    page.window_width = 550
    page.window_height = 250

    # Funciones de evento FilePickerResultEvent
    def pick_files_result(e: FilePickerResultEvent):
        text_up.value = (", ".join(map(lambda f: f.path, e.files)) if e.files else None)
        text_up.update()
        page.update()
    
    def save_files_result(e: FilePickerResultEvent):
        text_down.value = f"{e.path}.docx" if e.path else ""
        text_down.update()
    
    def verify_path(e):
        
        if text_up.value == "" and text_down.value == "":
            btn_up.bgcolor = "RED"
            btn_down.bgcolor = "RED"
            btn_down.update()
            btn_up.update()

        
        elif text_up.value == "" and text_down.value != "":
            btn_up.bgcolor = "RED"
            btn_down.bgcolor = "GREEN"
            btn_down.update()
            btn_up.update()

        
        elif text_up.value != "" and text_down.value == "":
            btn_up.bgcolor = "GREEN"
            btn_down.bgcolor = "RED"
            btn_down.update()
            btn_up.update()

        else:
            btn_up.bgcolor = "GREEN"
            btn_down.bgcolor = "GREEN"
            btn_up.disabled = True
            btn_down.disabled = True
            btn_convert.text = "Trabajando"
            btn_convert.disabled = True
            btn_down.update()
            btn_up.update()
            btn_convert.update()
            page.add(ProgressBar(width=400, color="amber", bgcolor="#eeeeee"))
            page.update()
            convert_file()
            page.controls.pop(3)
            page.update()
            btn_up.disabled = False
            btn_down.disabled = False
            btn_convert.disabled = False
            btn_convert.text = "Convertir"
            btn_down.update()
            btn_up.update()
            btn_convert.update()

    def convert_file():
        pdf_file = text_up.value
        docx_file = text_down.value
        # convert pdf to docx
        cv = Converter(pdf_file)
        cv.convert(docx_file)      # all pages by default
        cv.close()

    # Instancia de objetos FilePicker
    pick_files_dialog = FilePicker(on_result= pick_files_result)
    save_file_dialog = FilePicker(on_result= save_files_result)
    
    #Agregar a la ventana y mantenerlos Oculto
    page.overlay.extend([pick_files_dialog, save_file_dialog])

    # Componentes
    text_up = TextField(text_align='left', 
                        read_only= True, 
                        text_size= 9)

    text_down = TextField(text_align='left', 
                          text_size= 9, 
                          read_only= True)
    
    btn_up = ElevatedButton("Eleguir PDF", 
                            icon=icons.ARROW_CIRCLE_UP_OUTLINED, 
                            on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True, 
                                                                            allowed_extensions=['pdf'])
                            )
    
    btn_down = ElevatedButton("Ruta Descarga", icon=icons.ARROW_CIRCLE_DOWN,
                              on_click= lambda _: save_file_dialog.save_file(file_type='any', 
                                                                             allowed_extensions=['docx']))
    
    btn_convert = ElevatedButton("Convertir",
                                 icon= icons.BUILD_CIRCLE_SHARP,
                                 on_click= verify_path
                                 )

    #************************************************
    page.add(
        Row(
            [
                text_up,
                btn_up,
                pick_files_dialog
            ],
            alignment= 'right'
        ),
        Row(
            [
                text_down,
            btn_down,
            ],
            alignment= 'right'
        ),
        Row(
            [
                btn_convert
            ],
            alignment= "right"
        )
    )

app(target=main)