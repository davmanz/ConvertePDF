'''
import flet as ft
from flet import Page, app

def main(page:Page): 
    Page.title = 'Example'
    pr = ft.ProgressRing(width=50, height=50, stroke_width=5)
    page.add(pr)
app(main)
'''

blb = {1,2,3}

fas = blb.add(5)

print(blb)