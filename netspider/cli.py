"""Ana akis.

Akis: acilis -> banner -> root -> adaptor kontrolu -> monitor mod (+ gercek
arayuz tespiti) -> ag kesfi -> hedef secimi (numarali liste veya elle) ->
dinleme (arka planda) + saldiri (ayni terminalde) -> temizlik.

ASCII banner ve kullaniciya gorunen secim/prompt metinleri orijinalle aynidir;
degisen kisimlar guvenilirlik (arayuz tespiti) ve ergonomi (ag listesi) icindir.
"""

import os
import sys

from .ui.banner import BANNER
from .ui.animation import loading_animation
from .ui.colors import RED, YELLOW, WHITE_BOLD, BOLD, RESET
from .config import DEFAULT_INTERFACE, CAPTURE_DIR
from .core.process import run_popen_args, stop_process, force_cleanup
from .core.adapter import require_root, ensure_adapter, start_monitor
from .core.scanner import discover_networks
from .core.attack import run_attack
from .utils.validators import (
    validate_bssid, validate_channel, validate_capname, ValidationError,
)


def _select_target(networks):
    """Numarali liste sunar (varsa); elle giris secenegi korunur.

    (BSSID, CH) dondurur. Gecersiz girdide ValidationError yukseltir.
    """
    if networks:
        print(f"\n{WHITE_BOLD}--- BULUNAN AGLAR ---{RESET}")
        for i, net in enumerate(networks, 1):
            print(f"{BOLD}{i:>2}){RESET} {net['essid'][:24]:<24} "
                  f"{net['bssid']}  CH {net['channel']:<3} ({net['power']} dBm)")
        choice = input(BOLD + "\nNumara secin (elle girmek icin 'm'): " + RESET).strip().lower()
        if choice.isdigit() and 1 <= int(choice) <= len(networks):
            picked = networks[int(choice) - 1]
            return validate_bssid(picked["bssid"]), validate_channel(picked["channel"])

    # Elle giris (orijinal promptlar).
    print(f"\n{WHITE_BOLD}--- HEDEF SECIMI ---{RESET}")
    bssid = validate_bssid(input(BOLD + "Hedef BSSID (MAC): " + RESET))
    channel = validate_channel(input(BOLD + "Kanal (CH): " + RESET))
    return bssid, channel


def run():
    loading_animation()
    print(BANNER)

    require_root()
    ensure_adapter(DEFAULT_INTERFACE)
    iface = start_monitor(DEFAULT_INTERFACE)

    try:
        networks = discover_networks(iface)
    except Exception as e:
        print(RED + f"[-] Hata: {e}" + RESET)
        networks = []

    try:
        BSSID, CH = _select_target(networks)
        CAPNAME = validate_capname(input(BOLD + "Kayit Dosyasi Adi (orn: hedef_wifi): " + RESET))

        os.makedirs(CAPTURE_DIR, exist_ok=True)
        cap_prefix = os.path.join(CAPTURE_DIR, CAPNAME)

        print(YELLOW + f"\n[*] {BSSID} dinleniyor... Kayit: {CAPNAME}" + RESET)
        # Dinleme arka planda sessizce (TUI saldiri ekranini bozmasin).
        airodump_proc = run_popen_args(
            ["airodump-ng", iface, "--bssid", BSSID, "--channel", CH, "--write", cap_prefix],
            quiet=True,
        )

        # Saldiri ayni terminalde interaktif; ciktilar captures/ icinde toplanir.
        run_attack(BSSID, CAPNAME, iface, cwd=CAPTURE_DIR)

        stop_process(airodump_proc)

    except ValidationError as e:
        print(RED + f"[!] {e}" + RESET)
    except KeyboardInterrupt:
        pass

    force_cleanup(iface)


def main():
    try:
        run()
    except KeyboardInterrupt:
        force_cleanup(DEFAULT_INTERFACE)
        sys.exit(0)


if __name__ == "__main__":
    main()
