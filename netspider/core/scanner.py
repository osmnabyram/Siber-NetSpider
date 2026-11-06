"""Ag kesfi: airodump ile tarar, CSV'den ag listesini cikarir.

Orijinal scan_networks ile ayni etkilesim (canli tarama + ENTER ile durdurma),
ek olarak taranan aglari ayristirip numarali secim icin dondurur.
"""

import os
import tempfile
import time

from ..ui.colors import BOLD, YELLOW, RESET
from .process import run_popen_args, stop_process
from ..utils.airodump import parse_airodump_csv


def discover_networks(iface):
    print(BOLD + "[*] WiFi aglari taraniyor..." + RESET)
    print(YELLOW + "[!] Taramayi durdurmak ve hedef secmek icin ENTER tusuna basin." + RESET)

    tmpdir = tempfile.mkdtemp(prefix="netspider_scan_")
    prefix = os.path.join(tmpdir, "scan")

    # Canli TUI gorunur kalir; ayni anda CSV'ye de yazar.
    proc = run_popen_args(["airodump-ng", iface, "-w", prefix, "--output-format", "csv"])

    try:
        input()
    except KeyboardInterrupt:
        pass

    stop_process(proc)
    time.sleep(1)

    networks = parse_airodump_csv(prefix + "-01.csv")

    # Gecici dosyalari temizle
    try:
        for name in os.listdir(tmpdir):
            os.remove(os.path.join(tmpdir, name))
        os.rmdir(tmpdir)
    except OSError:
        pass

    print(YELLOW + "\n[*] Tarama durduruldu. Hedef secimine geciliyor..." + RESET)
    return networks
