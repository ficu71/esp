<!---[![License: MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/justcallmekoko/ESP32Marauder/blob/master/LICENSE)--->
<!---[![Gitter](https://badges.gitter.im/justcallmekoko/ESP32Marauder.png)](https://gitter.im/justcallmekoko/ESP32Marauder)--->
<!---[![Build Status](https://travis-ci.com/justcallmekoko/ESP32Marauder.svg?branch=master)](https://travis-ci.com/justcallmekoko/ESP32Marauder)--->
<!---Shields/Badges https://shields.io/--->

# ESP32 Marauder - ESP32-A1S Fork
<p align="center"><img alt="Marauder logo" src="https://github.com/justcallmekoko/ESP32Marauder/blob/master/pictures/marauder_skull_patch_04_full_final.png?raw=true" width="300"></p>
<p align="center">
  <b>A suite of WiFi/Bluetooth offensive and defensive tools for the ESP32</b>
  <br>
  <b>🎙️ Now with ESP32-A1S Audio Board Support! 🎙️</b>
  <br><br>
  <a href="https://github.com/justcallmekoko/ESP32Marauder/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
  <a href="https://gitter.im/justcallmekoko/ESP32Marauder"><img alt="Gitter" src="https://badges.gitter.im/justcallmekoko/ESP32Marauder.png"/></a>
  <br>
  <a href="https://twitter.com/intent/follow?screen_name=jcmkyoutube"><img src="https://img.shields.io/twitter/follow/jcmkyoutube?style=social&logo=twitter" alt="Twitter"></a>
  <a href="https://www.instagram.com/just.call.me.koko"><img src="https://img.shields.io/badge/Follow%20Me-Instagram-orange" alt="Instagram"/></a>
  <br><br>
</p>

## ✨ What's New in This Fork?

This fork adds **complete support for the ESP32-A1S Audio Board** (AI-Thinker Audio Kit) with the following features:

### 📦 Hardware Support
- ✅ **ES8388 Audio Codec** - Full I2S audio support
- ✅ **Dual Microphones** - Built-in mic input
- ✅ **Speaker Output** - Power amplifier control
- ✅ **6 Programmable Buttons** - Navigation and control
- ✅ **SD Card Slot** - Built-in microSD for PCAP storage
- ✅ **Optional TFT Display** - 240x320 ILI9341 support
- ✅ **Status LEDs** - Green/Red visual feedback

### 🛠️ What Works
✅ All standard ESP32 Marauder WiFi features  
✅ Beacon spam, deauth, probe sniffing  
✅ BLE scanning and attacks  
✅ PCAP capture to SD card  
✅ GPS logging (with external module)  
✅ Serial command interface  
✅ Audio codec initialization  
✅ Volume control via buttons  

### 🔥 Future Audio Features
🔄 Real-time audio spectrum analysis  
🔄 WiFi signal audio feedback  
🔄 Packet capture audio alerts  
🔄 Voice-controlled attacks  

## 🚀 Quick Start for ESP32-A1S

### Option 1: Pre-built Firmware (Coming Soon)
```bash
# Download firmware from releases
# Flash using esptool
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash 0x10000 marauder_esp32_a1s.bin
```

### Option 2: Build from Source

1. **Clone this repository**
```bash
git clone https://github.com/ficu71/esp.git
cd esp
git submodule update --init --recursive
```

2. **Enable ESP32-A1S in configs**

Edit `esp32_marauder/configs.h`:
```cpp
#define ESP32_A1S  // Uncomment this line
```

3. **Configure Arduino IDE**
- Board: "ESP32 Dev Module"
- Flash Size: "4MB (32Mb)"
- Partition Scheme: "Minimal SPIFFS"
- Upload Speed: "921600"

4. **Install Required Libraries**
- TFT_eSPI (by Bodmer)
- NimBLE-Arduino
- TinyGPS++
- LinkedList

5. **Copy TFT configuration**
```bash
cp User_Setup_esp32_a1s.h ~/Arduino/libraries/TFT_eSPI/User_Setup.h
```

6. **Compile and Upload**

Open `esp32_marauder/esp32_marauder.ino` in Arduino IDE and upload!

### 📚 Detailed Documentation

**For complete ESP32-A1S setup instructions, pinout diagrams, and troubleshooting:**

📝 **[Read the full ESP32-A1S Guide](ESP32_A1S_README.md)**

This includes:
- Complete pin mapping
- Hardware specifications
- Compilation instructions for both Arduino IDE and PlatformIO
- Audio codec configuration
- Troubleshooting guide
- Example code for audio features

## 📋 Hardware Requirements for ESP32-A1S Build

### Required:
- ESP32-A1S Audio Board (AI-Thinker)
- USB-C cable for programming
- MicroSD card (up to 32GB, FAT32)

### Optional:
- 2.8" or 3.2" ILI9341 TFT display (240x320)
- NEO-6M or similar GPS module
- External antenna for better WiFi range
- 4Ω 3W speaker (if not included)

## 📊 Pin Mapping Summary

| Function | GPIO Pin | Notes |
|----------|----------|-------|
| TFT CS | 15 | SPI shared with SD |
| TFT DC | 2 | |
| TFT RST | 4 | |
| TFT BL | 27 | PWM backlight |
| SD CS | 5 | Built-in SD slot |
| I2S MCLK | 0 | ES8388 codec |
| I2S BCK | 27 | ES8388 codec |
| I2S WS | 25 | ES8388 codec |
| I2S DOUT | 26 | To codec |
| I2S DIN | 35 | From codec |
| KEY1 (Left) | 36 | |
| KEY2 (Up) | 13 | |
| KEY4 (Right) | 23 | |
| KEY5 (Down) | 18 | |
| KEY6 (Select) | 5 | |
| LED Green | 22 | |
| LED Red | 19 | |

For complete pinout, see [ESP32_A1S_README.md](ESP32_A1S_README.md)

---

# Original ESP32 Marauder Information

[![Build and Push](https://github.com/justcallmekoko/ESP32Marauder/actions/workflows/build_push.yml/badge.svg)](https://github.com/justcallmekoko/ESP32Marauder/actions/workflows/build_push.yml)

## Getting Started
Download the [latest release](https://github.com/justcallmekoko/ESP32Marauder/releases/latest) of the firmware.  

Check out the project [wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki) for a full overview of the ESP32 Marauder

## For Sale Now
You can buy the original ESP32 Marauder hardware using [this link](https://www.justcallmekokollc.com)

---

## 🤝 Contributing

Contributions for ESP32-A1S improvements are welcome!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/audio-analyzer`)
3. Commit your changes (`git commit -am 'Add audio spectrum analyzer'`)
4. Push to the branch (`git push origin feature/audio-analyzer`)
5. Open a Pull Request

## ⚖️ Legal Notice

**IMPORTANT**: This tool is for educational purposes and authorized security testing only.  
Unauthorized attacks on WiFi networks are illegal. You are responsible for how you use this software.

## 📄 License

This project maintains the same MIT License as the original ESP32 Marauder.

## 👏 Credits

- **Original ESP32 Marauder**: [justcallmekoko](https://github.com/justcallmekoko/ESP32Marauder)
- **ESP32-A1S Port**: [ficu71](https://github.com/ficu71)
- **Hardware**: AI-Thinker ESP32-A1S Audio Kit

## 🔗 Useful Links

- [Original Marauder Wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki)
- [ESP32-A1S Detailed Guide](ESP32_A1S_README.md)
- [ES8388 Codec Datasheet](http://www.everest-semi.com/pdf/ES8388%20DS.pdf)
- [ESP32-A1S Hardware Repo](https://github.com/Ai-Thinker-Open/ESP32-A1S-AudioKit)

---

**Made with ❤️ for the security and maker community**
