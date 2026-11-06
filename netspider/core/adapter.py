"""Adaptor islemleri: root kontrolu, adaptor kontrolu, monitor mod + arayuz tespiti.

ONEMLI: Orijinalde arayuz her yerde sabit "wlan0" idi. Ama 'airmon-ng start'
sonrasi arayuz cogu sistemde "wlan0mon" olarak yeniden adlandirilir (bazen de
ayni kalir). Burada monitor moda gecildikten sonra sistemde GERCEKTEN monitor
modda olan arayuz 'iw' (yoksa 'iwconfig') ile tespit edilir ve bundan sonraki
tum islemler (tarama, dinleme, deauth, temizlik) o arayuz uzerinden yurur.
"""

import os
import subprocess
import sys
import time

from ..ui.colors import RED, GREEN, YELLOW, BOLD, RESET
from .process import run_cmd


def require_root():
    getuid = getattr(os, "getuid", None)
    if getuid is None:
        print(RED + "[!] Uyari: root kontrolu yalnizca Linux'ta yapilir." + RESET)
        return
    if getuid() != 0:
        print(RED + "[!] HATA: Root yetkisi (sudo) gereklidir." + RESET)
        sys.exit(1)


def _stdout(args):
    """Komutu shell'siz calistirip stdout dondurur; arac yoksa bos string."""
    try:
        result = subprocess.run(args, capture_output=True, text=True)
        return result.stdout or ""
    except FileNotFoundError:
        return ""


def list_wireless_interfaces():
    """Sistemdeki kablosuz arayuzleri listeler (once 'iw', sonra 'iwconfig')."""
    interfaces = []
    for line in _stdout(["iw", "dev"]).splitlines():
        line = line.strip()
        if line.startswith("Interface "):
            interfaces.append(line.split(None, 1)[1].strip())
    if interfaces:
        return interfaces

    # Yedek: iwconfig ciktisindan arayuz adlarini topla
    for line in _stdout(["iwconfig"]).splitlines():
        if line and not line[0].isspace() and "IEEE 802.11" in line:
            interfaces.append(line.split()[0])
    return interfaces


def interface_mode(iface):
    """Arayuzun modunu dondurur: 'monitor', 'managed' vb., yoksa None."""
    for line in _stdout(["iw", iface, "info"]).splitlines():
        line = line.strip()
        if line.startswith("type "):
            return line.split(None, 1)[1].strip()

    # Yedek: iwconfig
    out = _stdout(["iwconfig", iface])
    if "Mode:Monitor" in out:
        return "monitor"
    if "Mode:" in out:
        return "managed"
    return None


def detect_monitor_interface(base):
    """Monitor modda olan arayuzu bulur. Tercih sirasi: base+'mon', base, digerleri."""
    candidates = []
    for cand in (base + "mon", base):
        if cand not in candidates:
            candidates.append(cand)
    for iface in list_wireless_interfaces():
        if iface not in candidates:
            candidates.append(iface)

    for iface in candidates:
        if interface_mode(iface) == "monitor":
            return iface
    return None


def ensure_adapter(base):
    print(BOLD + f"[*] WiFi Adaptor ({base}) kontrol ediliyor..." + RESET)
    if interface_mode(base) is None and base not in list_wireless_interfaces():
        print(RED + f"[-] HATA: {base} adaptoru bulunamadi!" + RESET)
        sys.exit(1)
    print(GREEN + f"[+] {base} bulundu. Monitor modu baslatiliyor..." + RESET)


def start_monitor(base):
    """Monitor modu baslatir ve GERCEK monitor arayuzunu dondurur."""
    run_cmd(f"airmon-ng start {base}")
    time.sleep(2)

    monitor = detect_monitor_interface(base)
    if monitor is None:
        print(YELLOW + f"[!] Monitor arayuzu otomatik tespit edilemedi; '{base}' ile devam ediliyor." + RESET)
        return base
    if monitor != base:
        print(GREEN + f"[+] Monitor arayuzu tespit edildi: {monitor}" + RESET)
    else:
        print(GREEN + f"[+] Monitor modu aktif: {monitor}" + RESET)
    return monitor
