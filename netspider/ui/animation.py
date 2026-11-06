"""Acilis animasyonu (orijinal loading_animation ile ayni)."""

import itertools
import os
import sys
import time

from .colors import MENU_WHITE, GREEN, RESET
from ..config import INTRO_FRAMES, INTRO_DELAY


def loading_animation():
    os.system("clear")
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    print(f"{MENU_WHITE}Sistem aciliyor ", end="", flush=True)
    for _ in range(INTRO_FRAMES):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(INTRO_DELAY)
        sys.stdout.write("\b")
    print(f" {GREEN}Hosgeldiniz{RESET}\n")
    time.sleep(1)
    os.system("clear")
