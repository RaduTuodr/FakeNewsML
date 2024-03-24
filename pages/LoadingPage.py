import string
import time

import flet as ft

from mails import MailService
from pages.InfoPage import InfoPage


def LoadingPage(page: ft.Page, email: string, no_messages):

    page.clean()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 500

    email_input = ft.TextField(
        label="Email",
        disabled=True,
        hint_text="Email address",
        helper_text="Your email must be valid",
        prefix_icon=ft.icons.EMAIL_ROUNDED,
        suffix_text="...is your email address"
    )
    email_input.value = email

    submit_button = ft.ElevatedButton(text="Submit",
                                      disabled=True)

    progressBar = ft.ProgressBar(width=400)

    page.add(email_input, submit_button, progressBar)

    results = MailService.get_interpreted_messages(no_messages=no_messages)

    if results is not None:
        time.sleep(1.0)  # make progress bar visible in case of very fast mail fetching
        InfoPage(page=page, results=results, no_messages=no_messages)
