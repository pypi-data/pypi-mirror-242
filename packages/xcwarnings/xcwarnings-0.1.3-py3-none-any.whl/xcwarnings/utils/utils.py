"""
@File       utils.py
@Brief      Utils methods
@Author     cavacagu
@Date       12-02-2019
@copyright  Microsoft Corporation. All rights reserved.
"""
from . import console_colors

def print_success_message(message: str) -> None:
    """Prints a message in success format
    PARAMS:
    - message: Message to print
    """
    print(console_colors.ConsoleColors.OK + message + console_colors.ConsoleColors.END)

def print_error_message(message: str) -> None:
    """Prints a message in error format
    PARAMS:
    - message: Message to print
    """
    print(console_colors.ConsoleColors.ERROR + message + console_colors.ConsoleColors.END)

def print_warning_message(message: str) -> None:
    """Prints a message in error format
    PARAMS:
    - message: Message to print
    """
    print(console_colors.ConsoleColors.WARNING + message + console_colors.ConsoleColors.END)

def print_info_message(message: str) -> None:
    """Prints a message in info format
    PARAMS:
    - message: Message to print
    """
    print(console_colors.ConsoleColors.INFO + message + console_colors.ConsoleColors.END)
