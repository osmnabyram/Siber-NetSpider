<div align="center">

# NetSpider

### Guided Wi-Fi handshake capture and password-cracking workflow for labs and authorized testing.

A Python front-end for the Aircrack-ng suite that chains the usual manual steps — scan, capture, deauthenticate, crack — into one step-by-step terminal workflow.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Aircrack-ng](https://img.shields.io/badge/Built%20on-Aircrack--ng-e53935?style=for-the-badge)
![Purpose](https://img.shields.io/badge/Use-Authorized%20testing%20only-121212?style=for-the-badge)

</div>

<div align="center">
<img alt="NetSpider interface" src="https://github.com/user-attachments/assets/31f25032-a859-48a0-9ca5-693b2d66c9cf" />
</div>

---

## Overview

The Aircrack-ng workflow normally means remembering a chain of separate commands in the right order. NetSpider walks you through them from a single menu: it verifies the adapter, manages monitor mode, scans for networks, captures a handshake from a chosen access point, and hands the capture off for cracking. It is meant for **your own lab**, CTF practice, and engagements you are authorized to run.

---

## Workflow

| Step | Action |
|---|---|
| 1 | Verify the Wi-Fi adapter (`wlan0`) is present |
| 2 | Enable monitor mode via `airmon-ng` |
| 3 | Scan nearby Wi-Fi networks and list access points |
| 4 | Capture a WPA handshake from the selected target |
| 5 | Run deauthentication to prompt a client to reconnect |
| 6 | Validate the handshake and attempt a wordlist-based crack |

---

## Core Features

- Startup animation and ASCII banner
- Automatic Wi-Fi adapter (`wlan0`) verification
- Monitor-mode management (`airmon-ng`)
- Step-by-step guided terminal interface
- Single workflow from scan to crack

---

## Requirements

| Component | Notes |
|---|---|
| Python 3.x | Interpreter |
| Aircrack-ng suite | `airmon-ng`, `airodump-ng`, `aireplay-ng`, `aircrack-ng` |
| Compatible Wi-Fi adapter | Must support monitor mode and packet injection |
| Linux + root | Required for monitor mode and injection |

---

## Installation

```bash
git clone https://github.com/osmnabyram/Siber-NetSpider.git
cd Siber-NetSpider
chmod +x NetSpider.py
sudo python3 NetSpider.py
```

---

## Responsible Use

NetSpider is for **education, CTF competitions, lab setups, and authorized penetration testing only**. Capturing handshakes, deauthenticating clients, or cracking passwords on networks you do not own or are not explicitly authorized to test is illegal and unethical. The author accepts no responsibility for misuse.
