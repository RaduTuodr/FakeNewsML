from typing import List

import flet as ft


def InfoPage(page: ft.Page, messages: List[str], no_messages: int):
    page.clean()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 500

    cl = ft.Column(
        spacing=10,
        height=300,
        width=600,
        scroll=ft.ScrollMode.ALWAYS
    )

    for index in range(no_messages):
        container = ft.Container(
                ft.Text(messages[index]),
                border_radius=10,
                alignment=ft.alignment.top_left,
                padding=5,
                blur=10,
                height=100,
                key=str(index),

                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.colors.GREY_100, ft.colors.RED_200],
                ),
            )
        cl.controls.append(container)

    buttons = ft.Column([ft.Text("Scroll to:")])

    buttonRow = ft.Row()
    for index in range(no_messages):
        character = str(index)[0]
        button = ft.ElevatedButton(
            "Section " + character,
            on_click=lambda _: cl.scroll_to(key=character, duration=1000)
        )
        buttonRow.controls.append(button)

    buttons.controls.append(buttonRow)

    page.add(ft.Container(cl, border=ft.border.all(1)), buttons)
    page.update()
