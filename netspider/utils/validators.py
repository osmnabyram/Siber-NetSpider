"""Girdi dogrulama.

Orijinalde BSSID/kanal/dosya adi hic dogrulanmadan shell komutuna gomuluyordu.
Burada MAC/kanal/dosya adi bicimsel olarak dogrulanir; hem hatali girdi hem de
kabuk enjeksiyonu engellenir. Gecerli girdilerde davranis orijinalle aynidir.
"""

import re

MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
CH_RE = re.compile(r"^\d{1,3}$")
NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")


class ValidationError(ValueError):
    """Gecersiz kullanici girdisi."""


def validate_bssid(raw):
    value = (raw or "").strip()
    if not MAC_RE.match(value):
        raise ValidationError(f"Gecersiz BSSID (MAC bekleniyor, orn AA:BB:CC:DD:EE:FF): {raw!r}")
    return value


def validate_channel(raw):
    value = (raw or "").strip()
    if not CH_RE.match(value):
        raise ValidationError(f"Gecersiz kanal (1-3 haneli sayi bekleniyor): {raw!r}")
    return value


def validate_capname(raw):
    value = (raw or "").strip()
    if not NAME_RE.match(value):
        raise ValidationError(f"Gecersiz dosya adi (yalniz harf/rakam . _ -): {raw!r}")
    return value
