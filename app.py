from time import sleep
from pdf2docx import Converter
from flet import (app, Page, Row, TextField, icons, ElevatedButton, FilePickerResultEvent, FilePicker,
                  ProgressBar, Text, MainAxisAlignment, Column, AppBar, colors, View, RadioGroup, Radio)
from separate import split_pages
import os
from PyPDF2 import PdfReader

class appbar_edit:
    def __init__(self) -> None:
        txt_variable = txt_variable
        var = AppBar(
            title=Text(txt_variable),
            bgcolor=colors.SURFACE_VARIANT,
            center_title=True
        )
        return var

def main(page: Page):
    page.title = "PDF"
    #page.vertical_alignment = "center"
    page.window_width = 550
    page.window_height = 300
    page.window_resizable= False

    # INICIO---------------------------------------------------------------------------------------------
    appbar_init = AppBar(
        title=Text("Herramientas PDF"),
        bgcolor=colors.SURFACE_VARIANT,
        center_title=True
    )

    btn_init_converter= ElevatedButton("Conversor PDF", width=200, height=50, on_click= lambda _:page.go('/converter'))

    btn_init_join= ElevatedButton("Unir PDF", width=200, height=50)

    btn_init_separate= ElevatedButton("Separar PDF", width=200, height=50, on_click= lambda _:page.go('/separate'))

    btn_init_edit= ElevatedButton("Editar PDF", width=200, height=50)

    # FIN INICIO***********************************************************************************************  
    
    # CONVERSOR---------------------------------------------------------------------------------------------

    # FUNCIONES DE EVENTO FilePickerResultEvent
    def pick_files_result(e: FilePickerResultEvent):
        text_converter_up.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else None)
        global max_page
        max_page = len(PdfReader(text_converter_up.value).pages)
        text_converter_up.update()
        page.update()

    def save_files_result(e: FilePickerResultEvent):
        text_converter_down.value = f"{e.path}.docx" if e.path else ""
        text_converter_down.update()

    def out_dir_result(e: FilePickerResultEvent):
        text_converter_down.value = f"{e.path}" if e.path else ""
        text_converter_down.update()

    def verify_path(e):
        if text_converter_up.value == "" and text_converter_down.value == "":
            btn_converter_up.bgcolor = "RED"
            btn_converter_down.bgcolor = "RED"
            btn_converter_down.update()
            btn_converter_up.update()

        elif text_converter_up.value == "" and text_converter_down.value != "":
            btn_converter_up.bgcolor = "RED"
            btn_converter_down.bgcolor = "GREEN"
            btn_converter_down.update()
            btn_converter_up.update()

        elif text_converter_up.value != "" and text_converter_down.value == "":
            btn_converter_up.bgcolor = "GREEN"
            btn_converter_down.bgcolor = "RED"
            btn_converter_down.update()
            btn_converter_up.update()

        else:
            btn_converter_up.bgcolor = "GREEN"
            btn_converter_down.bgcolor = "GREEN"
            btn_converter_up.disabled = True
            btn_converter_down.disabled = True
            btn_converter.text = "Trabajando"
            btn_converter.disabled = True
            btn_converter_down.update()
            btn_converter_up.update()
            btn_converter.update()
            page.views[-1].controls.append(ProgressBar(width=400, color="amber", bgcolor="#eeeeee"))
            page.update()
            convert_file()
            page.views[-1].controls.pop(2)
            page.update()
            btn_converter_up.disabled = False
            btn_converter_down.disabled = False
            btn_converter.disabled = False
            btn_converter.text = "Convertir"
            btn_converter_down.update()
            btn_converter_up.update()
            btn_converter.update()

    # FUNCION CONVERTIR
    def convert_file():
        pdf_file = text_converter_up.value
        docx_file = text_converter_down.value
        # convert pdf to docx
        cv = Converter(pdf_file)
        cv.convert(docx_file)  # all pages by default
        cv.close()

    # Instancia de objetos FilePicker
    pick_files_dialog = FilePicker(on_result=pick_files_result)
    save_file_dialog = FilePicker(on_result=save_files_result)
    out_dir = FilePicker(on_result=out_dir_result)
    
    # Agregar a la ventana y mantenerlos Oculto
    page.overlay.extend([pick_files_dialog, save_file_dialog, out_dir])

    # Componentes
    appbar_converter = AppBar(
        title=Text("Conversor PDF > DOCX"),
        bgcolor=colors.SURFACE_VARIANT,
        center_title=True
    )

    text_converter_up = TextField(text_align="left", read_only=True, text_size=9)

    text_converter_down = TextField(text_align="left", text_size=9, read_only=True)

    btn_converter_up = ElevatedButton(
        "Eleguir PDF",
        icon=icons.ARROW_CIRCLE_UP_OUTLINED,
        on_click=lambda _: pick_files_dialog.pick_files(
            allow_multiple=True, allowed_extensions=["pdf"]
        )
    )

    btn_converter_down = ElevatedButton(
        "Ruta Descarga",
        icon=icons.ARROW_CIRCLE_DOWN,
        on_click=lambda _: save_file_dialog.save_file(
            file_type="any", allowed_extensions=["docx"]
        )
    )

    btn_converter = ElevatedButton(
        "Convertir", icon=icons.BUILD_CIRCLE_SHARP, on_click=verify_path
    )

    # FINAL CONVERSOR*********************************************************************************
    
    # SEPARADOR---------------------------------------------------------------------------------------

    # Componentes
    appbar_separate = AppBar(
        title=Text("Conversor PDF > DOCX"),
        bgcolor=colors.SURFACE_VARIANT,
        center_title=True
    )

    text_separate_page = TextField(
        text_align="left", 
        read_only=True, 
        text_size=14, 
        width=220, 
        on_change= lambda _:check_txt())

    btn_separate = ElevatedButton(
        "Separar", icon=icons.BUILD_CIRCLE_SHARP,
        disabled= True,
        on_click= lambda _: separate()
    )

    radius_separate_page = RadioGroup(content= Column([Radio(value= 'all', label= 'Todo'),
                                                        Radio(value= 'parts', label= 'Partes')]),
                                                        on_change= lambda _:change_radius(),                                                    
                                                        disabled= False
                                                        )

    btn_dir_down = ElevatedButton(
        "Ruta Descarga",
        icon=icons.ARROW_CIRCLE_DOWN,
        on_click=lambda _: out_dir.get_directory_path()
    )

    #Funciones

    def check_txt():
        content= text_separate_page.value
        character_permit ='0123456789,+-'

        if len(content) == 0:
            return
        
        if content[0] in ',+-':
            text_separate_page.value = ''
            page.update()
            return

        if content[-1] not in character_permit:
            text_separate_page.value = content[:len(content)-1]
            page.update()
        
        if content[len(content)-2:len(content)] in [
            '++','--',',,',
            '+-','-+',',+',
            '+,','-,',',-']:
            text_separate_page.value = content[:len(content)-1]
            page.update()

    def change_radius():

        text_separate_page.label = f'Max: {str(max_page)}'

        if radius_separate_page.value == 'all':
            text_separate_page.read_only = True
            btn_separate.disabled = False
        if radius_separate_page.value == 'parts':
            text_separate_page.read_only = False
            btn_separate.disabled = False
        page.update()
    
    def objet_blank(obj):
        obj.readonly = False
        obj.value = ''
        obj.readonly = True
       
    def separate():

        if text_converter_up.value == '' or text_converter_down.value == '':
            objet_blank(text_converter_up)
            objet_blank(text_converter_down)
            objet_blank(text_separate_page)
            page.update()
            return

        content= text_separate_page.value
        
        a = content.replace('+',',')
        b = a.replace('-',',')
        c = b.split(',')

        for x in c:
            if int(x) > max_page:
                text_separate_page.value = ''
                btn_separate.disabled = True
                radius_separate_page.value = None
                text_separate_page.read_only = True
                page.update()
                return
            
        if content[-1] in '-+,':
            text_separate_page.value = content[:len(content)-1]
            page.update()
        
        pages_extract = text_separate_page.value
        input = text_converter_up.value
        output = text_converter_down.value
        split_pages(input,output,pages_extract)
    
    # FINAL SEPARADOR***************************************************************************************
    # UNION---------------------------------------------------------------------------------------

    # FINAL UNION***********************************************************************************************

    # Pagina y Vistas******************************************************************************************
    
    def cambio_ruta(e):
        page.views.clear()

        page.views.append(
            View(
                '/',
                [
                    appbar_init,
                    Column([
                        Row([btn_init_converter, btn_init_edit], alignment=MainAxisAlignment.SPACE_EVENLY),
                        Row([btn_init_join, btn_init_separate], alignment=MainAxisAlignment.SPACE_EVENLY)
                    ], spacing=35)
                ]        
            )           
        )
        
        if page.route == '/converter':
            page.views.append(
                View(
                    '/converter',
                    [
                        appbar_converter,
                        Column([
                            Row([text_converter_up, btn_converter_up], alignment= 'right'),
                            Row([text_converter_down, btn_converter_down], alignment= 'right'),
                            Row([btn_converter], alignment= "right")
                        ])
                    ]          
                )      
            )
        
        if page.route == '/separate':
            page.views.append(
                View(
                    '/separate',
                    [
                        appbar_separate,
                        Column([
                            Row([text_converter_up, btn_converter_up], alignment= 'right'),
                            Row([text_converter_down, btn_dir_down]),
                            Row([radius_separate_page,text_separate_page, btn_separate], alignment= "right")
                        ])
                    ]
                )
            )
        
        page.update()

    def quitar_vista(view):
        page.views.pop()
        pagina_superior = page.views[-1]
        page.go(pagina_superior.route)

    page.on_route_change = cambio_ruta
    page.on_view_pop = quitar_vista
    page.go(page.route)

app(target=main)
