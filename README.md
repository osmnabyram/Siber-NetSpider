# WiFi Handshake and Deauthentication Automation Tool

This project is a **Python-based** cybersecurity tool built on the **Aircrack-ng** toolset that automates the **handshake capture**, **deauthentication**, and **password cracking** processes on Wi-Fi networks in a semi-automated manner.

The tool simplifies command chains that would otherwise require manual execution, providing practical utility in **educational environments**, **CTF competitions**, **lab setups**, and **authorized penetration testing** scenarios.

![image](https://github.com/user-attachments/assets/31f25032-a859-48a0-9ca5-693b2d66c9cf)

---

## General Purpose

- Scan Wi-Fi networks
- Capture handshakes from target access points
- Automate deauthentication attacks
- Execute handshake validation and password cracking in a single workflow
- Guide users step-by-step through the terminal interface

---

## Core Features

- Startup animation and ASCII banner
- Automatic Wi-Fi adapter (`wlan0`) verification
- Monitor mode management (`airmon-ng`)
- Live Wi-Fi network scanning (`airodump-ng`)
- Target listening based on BSSID and channel
- Separate terminal deauthentication management
- Handshake validation (`aircrack-ng`)
- Brute-force automation (`crunch + john + aircrack-ng`)
- Process termination and clean shutdown support

---

## Tools Used

- Python 3
- Bash
- Aircrack-ng
  - airmon-ng
  - airodump-ng
  - aireplay-ng
  - aircrack-ng
- Crunch
- John the Ripper
- Linux-based operating system

---

## Requirements

The following must be installed on the system for the tool to function:

- Linux (Kali, Parrot, Ubuntu, etc.)
- Python 3.x
- Aircrack-ng
- Crunch
- John the Ripper
- Wi-Fi adapter with monitor mode support
- gnome-terminal

---

## Installation
```bash
git clone https://github.com/osmnabyram/NetSpider.git
cd NetSpider
chmod +x netspider.py
```

## Usage

The tool requires **root privileges** to execute:
```bash
sudo python3 netspider.py
```

## Workflow

- Wi-Fi adapter is verified
- Monitor mode is activated
- Surrounding Wi-Fi networks are listed
- Target BSSID, channel, and capture file name are entered
- Target is placed under surveillance
- Deauthentication is executed in a separate terminal
- Upon handshake capture, validation and password cracking commence
- Monitor mode is disabled at process completion

## Example Usage Scenario

- A WPA/WPA2 network is identified in a lab environment
- Clients are disconnected via deauthentication
- Handshake is captured
- Password security is tested
- Results are analyzed

## Legal Notice

This tool is designed exclusively for **educational purposes**, **CTF competitions**, **lab environments**, and **authorized penetration testing** scenarios.

Use against unauthorized networks or systems is **illegal** and incurs legal liability.

The developer assumes **no responsibility** for any damages resulting from misuse of this tool.
