import flet as ft

from pages.LoadingPage import LoadingPage
from utils import validate_email


def EmailPage(page: ft.Page):
    page.clean()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 500

    def valid_email(event):
        return validate_email(email_input.value)

    email_input = ft.TextField(
        label="Email",
        hint_text="Email address",
        helper_text="Your email must be valid",
        prefix_icon=ft.icons.EMAIL_ROUNDED,
        suffix_text="...is your email address"
    )

    def on_button_click(event):
        if valid_email(email_input.value):
            email_input.helper_style = ft.TextStyle()
            LoadingPage(page, email_input.value)
        else:
            email_input.helper_text = "Invalid email"
            email_input.helper_style = ft.TextStyle(color=ft.colors.RED)
        page.update()

    submit_button = ft.ElevatedButton(text="Submit",
                                      on_click=on_button_click)

    page.add(email_input, submit_button)
