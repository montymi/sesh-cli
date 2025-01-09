#!/usr/bin/env python
"""
Example of a message box window that takes user input and displays it.
"""

from prompt_toolkit.shortcuts import message_dialog, input_dialog
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Box, Button, Label


def show_message_dialog(title, text):
    bindings = KeyBindings()

    @bindings.add('enter')
    def _(event):
        event.app.exit()

    dialog = Box(
        HSplit([
            Label(text=text),
            Button(text="OK", handler=lambda: app.exit())
        ]OBOB),
        padding=1,
        style='class:dialog.body'
    )

    layout = Layout(dialog)

    app = Application(layout=layout, key_bindings=bindings, full_screen=True)
    app.run()


def main():
    # Get user input
    user_input = input_dialog(
        title="Input Dialog",
        text="Please enter your input:",
    ).run()

    if user_input is not None:
        # Display the input in a message dialog
        show_message_dialog(
            title="Example dialog window",
            text=f"You entered: {user_input}\nPress ENTER to quit."
        )


if __name__ == "__main__":
    main()

