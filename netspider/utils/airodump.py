"""airodump-ng CSV ciktisini ayristirir (hedef secim listesi icin)."""

from .validators import MAC_RE


def parse_airodump_csv(path):
    """CSV'den AP listesini okur. Her biri: bssid, channel, power, essid.

    airodump CSV'si iki bolumden olusur (AP'ler ve istasyonlar); sadece AP
    bolumu okunur. Hatali/baslik satirlari BSSID bicimine gore elenir.
    """
    networks = []
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except (FileNotFoundError, OSError):
        return networks

    ap_section = text.split("Station MAC")[0]
    for line in ap_section.splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 14:
            continue
        bssid = parts[0]
        if not MAC_RE.match(bssid):   # baslik satiri / cop -> atla
            continue
        networks.append({
            "bssid": bssid,
            "channel": parts[3],
            "power": parts[8],
            "essid": parts[13] or "<gizli>",
        })
    return networks
