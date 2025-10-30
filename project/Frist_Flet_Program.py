import flet as ft

def main(page: ft.Page):
    page.title = "Hello Flet!"
    page.add(ft.Text("Welcome to Kawsar's Flet App!", size=30))

ft.app(target=main)
