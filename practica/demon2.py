import flet

from flet import AppBar, ElevatedButton, Page, Text, View, colors

def main(page: Page):
    page.title = 'Ejemplo Rutas'

    def cambio_ruta(e):
        page.views.clear()

        page.views.append(
            View(
                '/',
                [
                    AppBar(title= Text('01 Flet App'), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton('Visitar Store', on_click= lambda _:page.go('/store'))
                ]          
            )           
        )
        
        if page.route == '/store':
            page.views.append(
            View(
                '/store',
                [
                    AppBar(title= Text('02 Tienda'), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton('Inicio', on_click= lambda _:page.go('/'))
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

flet.app(target=main)