import flet as ft

import utils

currentScrollPosition = 0.0


def handle_scrolling(event):
    global currentScrollPosition
    currentScrollPosition = event.pixels


def getNextKey():
    character = '0'
    index = int(currentScrollPosition / 110)
    return chr(ord(character) + index + 1)


def InfoPage(page: ft.Page, results: dict, no_messages: int):
    page.clean()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width  = utils.WINDOW_WIDTH
    page.window_height = utils.WINDOW_HEIGHT

    messagesColumn = ft.Column(
        spacing=10,
        height=300,
        width=600,
        scroll=ft.ScrollMode.ALWAYS,

        on_scroll=handle_scrolling
    )

    messages = results['messages']
    predictions = results['predictions']

    for index in range(no_messages):

        if predictions[index] == 0:
            colors = [ft.colors.GREY_100, ft.colors.RED_200]
        else:
            colors = [ft.colors.GREY_100, ft.colors.GREEN_200]

        gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=colors
        )

        container = ft.Container(
            ft.Text(messages[index]),
            border_radius=10,
            alignment=ft.alignment.top_left,
            padding=0,
            blur=10,
            height=100,
            key=str(index),

            gradient=gradient
        )
        messagesColumn.controls.append(container)

    nextButton = ft.ElevatedButton(
        "Next mail",
        on_click=lambda _: messagesColumn.scroll_to(key=getNextKey(), duration=750),
        expand=True,  # Allows the button to expand to the full width of its parent container
    )

    buttonRow = ft.Row(
        width=600
    )
    buttonRow.controls.append(nextButton)

    layout = ft.Column(
        controls=[
            ft.Container(messagesColumn,
                         border=ft.border.all(1)),
            buttonRow,
        ],
        expand=True,  # Ensures the column expands to fill its parent container
    )

    page.add(layout)
