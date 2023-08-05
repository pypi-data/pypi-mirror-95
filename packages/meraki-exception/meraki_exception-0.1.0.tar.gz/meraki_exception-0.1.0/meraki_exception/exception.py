import sys
import meraki
from rich.console import Console
from rich.theme import Theme
## Config de rich
custom_theme = Theme({"good": "green", "bad": "bold red"})
console = Console(theme=custom_theme)


def meraki_exception(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except meraki.APIError as e:
            console.print(f'Meraki API error: {e}')
            console.print(f'status code = {e.status}')
            console.print(f'reason = {e.reason}')
            console.print(f'error = {e.message}')
            console.print("Please correct the error and start over.", style="bad")
            sys.exit(1)
        except Exception as e:
            console.print(f'some other error: {e}')
            console.print("Please correct the error and start over.", style="bad")
            sys.exit(1)
    return inner_function