import flet as ft

import utils
from pages.LoadingPage import LoadingPage
from utils import validate_email


def EmailPage(page: ft.Page):
    page.clean()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = utils.WINDOW_WIDTH
    page.window_height = utils.WINDOW_HEIGHT

    def valid_email(event):
        return validate_email(email_input.value)

    email_input = ft.TextField(
        label="Email",
        hint_text="Email address",
        helper_text="Your email must be valid",
        prefix_icon=ft.icons.EMAIL_ROUNDED,
        suffix_text="...is your email address"
    )

    def slider_change(event):

        if slider.value is None:
            return

        no_messages.value = "How many emails to check: "
        value = slider.value
        if value == 0:
            no_messages.value += "5"
        elif value == 1:
            no_messages.value += "25"
        elif value == 2:
            no_messages.value += "100"
        else:
            no_messages.value += "500"
        page.update()

    no_messages = ft.Text("How many emails to check: 5")

    slider = ft.CupertinoSlider(
        divisions=3,
        max=3,
        active_color=ft.colors.GREY_200,
        thumb_color=ft.colors.GREY_300,
        on_change=slider_change
    )

    def on_button_click(event):
        if valid_email(email_input.value):
            email_input.helper_style = ft.TextStyle()
            LoadingPage(page, email_input.value, int(''.join([char for char in no_messages.value if char.isdigit()])) )
        else:
            email_input.helper_text = "Invalid email"
            email_input.helper_style = ft.TextStyle(color=ft.colors.RED)
        page.update()

    submit_button = ft.ElevatedButton(text="Submit",
                                      on_click=on_button_click)

    main_column = ft.Column(
        controls=[
            email_input,
            slider,
            no_messages,
            submit_button,
        ],
        spacing=20
    )

    page.add(main_column)
