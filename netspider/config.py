"""Merkezi yapilandirma."""

# Baslangicta monitor moda alinacak varsayilan arayuz.
# Monitor moda gectikten SONRA gercek arayuz adi (orn. wlan0mon) calisma aninda
# sistemden tespit edilir; bu yalnizca baslangic adaptorudur.
DEFAULT_INTERFACE = "wlan0"

# Yakalama ciktilarinin (.cap, anahtar, oturum) toplanacagi klasor.
CAPTURE_DIR = "captures"

# Acilis animasyonu
INTRO_FRAMES = 20
INTRO_DELAY = 0.15
