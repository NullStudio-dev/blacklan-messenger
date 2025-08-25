from colorama import Fore, Style

class Colors:
    INFO = Fore.BLUE + Style.BRIGHT + '[INFO]' + Style.RESET_ALL
    OK = Fore.GREEN + Style.BRIGHT + '[ OK ]' + Style.RESET_ALL
    ERROR = Fore.RED + Style.BRIGHT + '[ ERROR ]' + Style.RESET_ALL
    WARNING = Fore.YELLOW + Style.BRIGHT + '[WARN]' + Style.RESET_ALL
    DEBUG = Fore.MAGENTA + Style.BRIGHT + '[DEBUG]' + Style.RESET_ALL
    RESET = Style.RESET_ALL

    def colorize(self, text, color):
        return color + text + Style.RESET_ALL


