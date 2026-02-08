# ESP32-A1S Support for ESP32 Marauder

## 📋 Przegląd

Ten fork ESP32 Marauder dodaje pełne wsparcie dla modułu **ESP32-A1S (AI Thinker Audio Kit)** - płytki developmentowej z wbudowanym kodekiem audio ES8388.

## 🔧 Specyfikacja Hardware

### ESP32-A1S Features:
- **Główny chip**: ESP32-WROOM-32
- **Kodek audio**: ES8388 (I2S interface)
- **Mikrofony**: 2x wbudowane mikrofony
- **Wyjście audio**: Wbudowany wzmacniacz + złącze głośnikowe
- **Slot SD**: Wbudowany czytnik microSD
- **Przyciski**: 6x przycisków programowalnych (KEY1-KEY6)
- **LEDy**: 2x LED (zielony + czerwony)
- **Interfejsy**: I2C, I2S, SPI, UART

## 📌 Mapowanie Pinów

### Wyświetlacz TFT (opcjonalny)
```
TFT_MISO = 12
TFT_MOSI = 13
TFT_SCLK = 14
TFT_CS   = 15
TFT_DC   = 2
TFT_RST  = 4
TFT_BL   = 27  // Podświetlenie PWM
TOUCH_CS = 33  // Ekran dotykowy
```

### Karta SD (wbudowana)
```
SD_CS   = 5
SD_MISO = 12  // Współdzielony z TFT
SD_MOSI = 13  // Współdzielony z TFT
SD_SCK  = 14  // Współdzielony z TFT
```

### Kodek Audio ES8388 (I2S)
```
PIN_I2S_MCLK = 0   // Master clock
PIN_I2S_BCK  = 27  // Bit clock
PIN_I2S_WS   = 25  // Word select (LRCLK)
PIN_I2S_DOUT = 26  // Data out (do kodeka)
PIN_I2S_DIN  = 35  // Data in (z kodeka)
```

### Kontrola ES8388 (I2C)
```
ES8388_I2C_SDA  = 33
ES8388_I2C_SCL  = 32
ES8388_I2C_ADDR = 0x10
```

### Przyciski Nawigacyjne
```
L_BTN (KEY1)  = 36  // Lewo
U_BTN (KEY2)  = 13  // Góra
R_BTN (KEY4)  = 23  // Prawo
D_BTN (KEY5)  = 18  // Dół
C_BTN (KEY6)  = 5   // Center/Select
KEY3          = 19  // Dodatkowy przycisk
```

### Diody LED
```
LED_GREEN = 22
LED_RED   = 19  // Może kolidować z KEY3
```

### Wzmacniacz Audio
```
PA_EN_PIN = 21  // Power Amplifier Enable
```

### GPS (opcjonalny - zewnętrzny moduł)
```
GPS_TX = 17  // GPIO TX dla GPS
GPS_RX = 16  // GPIO RX dla GPS
```

## 🚀 Kompilacja i Flash

### Krok 1: Przygotowanie środowiska

```bash
# Klonuj repozytorium
git clone https://github.com/ficu71/esp.git
cd esp

# Zainstaluj wymagane submoduły
git submodule update --init --recursive
```

### Krok 2: Konfiguracja Arduino IDE

1. Zainstaluj **Arduino IDE 1.8.19+** lub **Arduino IDE 2.x**
2. Dodaj ESP32 board manager URL:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Zainstaluj **ESP32 by Espressif** (wersja 2.0.14 lub nowsza)
4. Wybierz płytkę: **ESP32 Dev Module**

### Krok 3: Włącz ESP32-A1S Support

Edytuj `esp32_marauder/configs.h`:

```cpp
// Znajdź sekcję BOARD TARGETS i odkomentuj:
#define ESP32_A1S  // ESP32-A1S Audio Board with ES8388 codec

// Zakomentuj wszystkie inne definicje boardów
```

### Krok 4: Konfiguracja Kompilacji

**Arduino IDE Settings:**
```
Board: "ESP32 Dev Module"
Upload Speed: "921600"
CPU Frequency: "240MHz (WiFi/BT)"
Flash Frequency: "80MHz"
Flash Mode: "QIO"
Flash Size: "4MB (32Mb)"
Partition Scheme: "Minimal SPIFFS (1.9MB APP with OTA/190KB SPIFFS)"
Core Debug Level: "None"
PSRAM: "Disabled" (ESP32-A1S nie ma PSRAM)
```

### Krok 5: Wymagane Biblioteki

Zainstaluj następujące biblioteki przez Arduino Library Manager:

```
- TFT_eSPI (by Bodmer) - dla wyświetlacza
- SD (wbudowana w ESP32)
- WiFi (wbudowana w ESP32)
- NimBLE-Arduino (dla BLE)
- TinyGPS++ (dla GPS)
- LinkedList (by Ivan Seidel)
```

### Krok 6: Konfiguracja TFT_eSPI

Skopiuj plik konfiguracyjny:
```bash
cp User_Setup_esp32_a1s.h ~/Arduino/libraries/TFT_eSPI/User_Setup.h
```

Lub ręcznie edytuj `User_Setup_Select.h` w bibliotece TFT_eSPI:
```cpp
#include <User_Setups/User_Setup_esp32_a1s.h>
```

### Krok 7: Kompilacja

1. Otwórz `esp32_marauder/esp32_marauder.ino` w Arduino IDE
2. Sprawdź czy nie ma błędów w zakładce konsoli
3. Kliknij **Verify/Compile** (✓)
4. Sprawdź wykorzystanie pamięci - powinno być poniżej 100%

### Krok 8: Flash do ESP32-A1S

```bash
# Podłącz ESP32-A1S przez USB
# Sprawdź port (Linux/Mac: /dev/ttyUSB0, Windows: COM3)

# Flash używając Arduino IDE
# Lub użyj esptool:

esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash -z 0x1000 bootloader.bin \
  0x8000 partitions.bin \
  0x10000 esp32_marauder.bin
```

## 🎛️ Konfiguracja Dodatkowa

### Włączenie Audio Features

Jeżeli chcesz wykorzystać funkcje audio ES8388, musisz:

1. Dodać bibliotekę ES8388:
```bash
cd esp32_marauder/libraries
git clone https://github.com/atomic14/esp32-i2s-audio.git
```

2. Zmodyfikować kod aby używać funkcji audio:
```cpp
#ifdef HAS_AUDIO_CODEC
  // Inicjalizacja ES8388
  Wire.begin(ES8388_I2C_SDA, ES8388_I2C_SCL);
  // ... kod inicjalizacji kodeka
#endif
```

### Dodanie GPS

Podłącz zewnętrzny moduł GPS:
- GPS TX → GPIO 16 (ESP32 RX)
- GPS RX → GPIO 17 (ESP32 TX)
- GPS VCC → 3.3V
- GPS GND → GND

## 📊 Funkcjonalności

### Obsługiwane przez ESP32-A1S:
✅ WiFi scanning i sniffing  
✅ Beacon spam attacks  
✅ Deauth attacks  
✅ Probe request sniffing  
✅ Evil portal  
✅ BLE scanning  
✅ Packet monitor (PCAP)  
✅ Zapis do karty SD  
✅ Interfejs szeregowy  
✅ GPS logging (z zewnętrznym modułem)  

### W przyszłości (Audio features):
🔄 Nagrywanie audio przez mikrofony  
🔄 Analiza spektrum audio  
🔄 Audio feedback dla ataków  
🔄 Detekcja dźwięków sieci  

## 🐛 Troubleshooting

### Problem: Nie mogę wgrać firmware
**Rozwiązanie**: 
- Przytrzymaj przycisk BOOT podczas podłączania USB
- Sprawdź czy wybrałeś właściwy port COM
- Spróbuj niższej prędkości upload (115200)

### Problem: Wyświetlacz nie działa
**Rozwiązanie**:
- Sprawdź czy TFT jest prawidłowo podłączony
- Zweryfikuj konfigurację pinów w User_Setup_esp32_a1s.h
- Sprawdź czy TFT_BL (backlight) jest na wysokim stanie

### Problem: Karta SD nie jest wykrywana
**Rozwiązanie**:
- Sformatuj kartę jako FAT32
- Użyj karty o pojemności max 32GB
- Sprawdź połączenia SPI

### Problem: Brak GPS fix
**Rozwiązanie**:
- Sprawdź czy moduł GPS jest podłączony prawidłowo
- Wyjdź na zewnątrz dla lepszego sygnału
- Sprawdź czy GPS TX/RX nie są zamienione

### Problem: Bluetooth nie działa
**Rozwiązanie**:
- Upewnij się że NimBLE-Arduino jest zainstalowana
- WiFi i BT współdzielą zasoby - spróbuj wyłączyć WiFi

## 📝 Przykładowe Komendy

### Przez Serial Monitor (115200 baud):

```bash
# Skanowanie WiFi
scan -t ap

# Beacon spam
attack -t beacon -ssid "TEST_AP"

# Deauth attack
attack -t deauth -c 6

# Lista podłączonych stacji
list -t ap

# Zapis do karty SD
pcap -s

# BLE scan
scan -t ble
```

## 🔗 Zasoby

- [ESP32-A1S Schematic](https://github.com/Ai-Thinker-Open/ESP32-A1S-AudioKit)
- [ES8388 Datasheet](http://www.everest-semi.com/pdf/ES8388%20DS.pdf)
- [ESP32 Marauder Wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki)
- [TFT_eSPI Documentation](https://github.com/Bodmer/TFT_eSPI)

## 🤝 Contributing

Jeżeli masz sugestie lub znalazłeś bugi:
1. Otwórz Issue na GitHubie
2. Opisz szczegółowo problem
3. Załącz logi z Serial Monitor
4. Pull requesty są mile widziane!

## ⚖️ Legal Notice

**WAŻNE**: To narzędzie służy wyłącznie do celów edukacyjnych i testowania własnych sieci. 
Nieautoryzowane ataki na sieci WiFi są nielegalne. Użytkownik ponosi pełną odpowiedzialność 
za sposób wykorzystania tego oprogramowania.

## 📄 Licencja

MIT License - zobacz [LICENSE](LICENSE) dla szczegółów

---

**Autor**: ficu71  
**Based on**: [ESP32 Marauder](https://github.com/justcallmekoko/ESP32Marauder) by justcallmekoko  
**Hardware**: ESP32-A1S by AI-Thinker
