#!/usr/bin/env python
"""
Demonstration of a custom completer wrapped in a `FuzzyCompleter` for fuzzy
matching.
"""

from prompt_toolkit.completion import Completer, Completion, FuzzyCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt

services = [
    "help",
    "habits",
    "model",
    "import",
    "export",
    "clean",
    "save"
]


class ColorCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for service in services:
            if service.startswith(word):
                yield Completion(
                    service,
                    start_position=-len(word),
                    style="fg:" + "purple",
                    selected_style="fg:white bg:" + "purple",
                )


def main():
    # Simple completion menu.
    print("(The completion menu displays colors.)")
    prompt("Type a color: ", completer=FuzzyCompleter(ColorCompleter()))

    # Multi-column menu.
    prompt(
        "Type a color: ",
        completer=FuzzyCompleter(ColorCompleter()),
        complete_style=CompleteStyle.MULTI_COLUMN,
    )

    # Readline-like
    prompt(
        "Type a color: ",
        completer=FuzzyCompleter(ColorCompleter()),
        complete_style=CompleteStyle.READLINE_LIKE,
    )


if __name__ == "__main__":
    main()
