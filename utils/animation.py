import time
import sys
from colorama import Fore, Style

class Animation:
    @staticmethod
    def spinner(duration=3, message="Loading"):
        """Display a spinner animation"""
        spinner_chars = ["|", "/", "-", "\\"]
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{Fore.CYAN}[{spinner_chars[i % len(spinner_chars)]}] {message}...{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + " " * 50 + "\r")  # Clear the line
        sys.stdout.flush()

    @staticmethod
    def typewriter(text, delay=0.05):
        """Display text with typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def progress_bar(duration=3, message="Processing"):
        """Display a progress bar"""
        bar_length = 30
        for i in range(bar_length + 1):
            percent = (i / bar_length) * 100
            bar = "█" * i + "░" * (bar_length - i)
            sys.stdout.write(f"\r{Fore.GREEN}[{bar}] {percent:.1f}% {message}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(duration / bar_length)
        print()

