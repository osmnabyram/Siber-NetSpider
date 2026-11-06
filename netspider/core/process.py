"""Alt surec yonetimi: calistirma, durdurma, acil temizlik."""

import os
import signal
import subprocess

from ..ui.colors import RED, GREEN, RESET


def run_cmd(cmd, block=True):
    """Sabit (kullanici girdisi icermeyen) kabuk komutlari icin."""
    if block:
        return subprocess.run(cmd, shell=True)
    return subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)


def run_popen_args(args, quiet=False):
    """Kullanici girdisi iceren komutlar icin shell'siz surec baslatir.

    args bir liste oldugundan ve girdiler dogrulandigindan kabuk enjeksiyonu
    mumkun degildir. setsid ile ayni surec grubunda baslatilir ki stop_process
    temiz sekilde sonlandirabilsin. quiet=True iken ciktisi bastirilir (ornegin
    saldiri sirasinda arka planda sessizce kayit alan airodump icin).
    """
    kwargs = {"preexec_fn": os.setsid}
    if quiet:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
    return subprocess.Popen(args, **kwargs)


def stop_process(proc):
    if proc is None:
        return
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except (ProcessLookupError, AttributeError, OSError):
        pass


def force_cleanup(iface=None):
    print(RED + "\n[!] ACIL TEMIZLIK: Arka plan islemleri sonlandiriliyor..." + RESET)
    try:
        subprocess.run("killall airodump-ng aireplay-ng aircrack-ng 2>/dev/null", shell=True)
        if iface:
            subprocess.run(f"airmon-ng stop {iface} > /dev/null 2>&1", shell=True)
        subprocess.run("service network-manager restart", shell=True)
    except Exception as e:
        print(f"[-] Temizlik sirasinda hata: {e}")
    print(GREEN + "[+] Sistem temizlendi." + RESET)
