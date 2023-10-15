import flet
from flet import AppBar, ElevatedButton, Page,Text,View,colors

def main(page:Page):
    page.title = 'Ejemplo Rutas'

    print('Ruta inicial:', page.route)

    def cambio_ruta(e):

        print('Ruta Cambiada:', e.route)
        page.views.clear()
        page.views.append(
            View(
                '/',
                [
                    AppBar(title=Text('01 Flet app')),
                    ElevatedButton('Ir a configuracion', on_click = open_settins)
                ]
            )
        )
        if page.route == '/settings' or page.route == '/settings/mail':
            page.views.append(
                View(
                    '/settings',
                    [
                    AppBar(title= Text('02 Settings', bgcolor= colors.SURFACE_VARIANT)),
                    Text('Configuracion', style= 'bodyMedium'),
                    ElevatedButton('Ir a configuracion de Mail', on_click= open_mail_settings)
                    ]
                     )
            )

        if page.route == '/settings/mail':
            page.views.append(
                View(
                    '/settings/mail',
                    [
                    AppBar(title= Text('03 Flet App', bgcolor= colors.SURFACE_VARIANT)),
                    Text('Mail Settings', style= 'bodyMedium')
                    ]
                     )
            )
        page.update()

    def cambio_pagina(e):
        print('View pop:', e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = cambio_ruta
    page.on_view_pop = cambio_pagina

    def open_mail_settings(e):
        page.go('/settings')

    def open_settins(e):
        page.go('/settings/mail')

    page.go(page.route)

flet.app(target= main)