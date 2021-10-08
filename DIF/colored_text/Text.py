from colorama import Fore, Style, init

__all__ = ["Text"]

init()


class Text:
    EXC = Fore.BLUE + Style.BRIGHT + "[!]" + Style.RESET_ALL
    CROSS = Fore.RED + Style.BRIGHT + "[✗]" + Style.RESET_ALL
    TICK = Fore.GREEN + Style.BRIGHT + "[✔]" + Style.RESET_ALL
    INFO = Fore.BLUE + Style.BRIGHT + "[INFO]" + Style.RESET_ALL
    DONE = Fore.GREEN + Style.BRIGHT + "[DONE]" + Style.RESET_ALL
    ERROR = Fore.RED + Style.BRIGHT + "[ERROR]" + Style.RESET_ALL
    WARN = Fore.YELLOW + Style.BRIGHT + "[WARN]" + Style.RESET_ALL
    LOADING = Fore.MAGENTA + Style.BRIGHT + "[%]" + Style.RESET_ALL
    PROCESSING = Fore.MAGENTA + Style.BRIGHT + "[⚙]" + Style.RESET_ALL
