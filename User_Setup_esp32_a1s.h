// ESP32-A1S Audio Board Configuration for ESP32 Marauder
// This board uses ES8388 audio codec with I2S interface
// Created for ESP32-A1S module support

// ##################################################################################
//
// ESP32-A1S (AI Thinker Audio Kit) configuration
// This module includes:
// - ES8388 audio codec
// - Dual microphones
// - Speaker output
// - SD card slot
// - Buttons and LEDs
//
// ##################################################################################

#define USER_SETUP_INFO "User_Setup_esp32_a1s"

// Driver selection - using ILI9341 as commonly paired with ESP32-A1S
#define ILI9341_DRIVER

// ESP32-A1S specific pins
// Display pins (if using external TFT)
#define TFT_MISO 12
#define TFT_MOSI 13  
#define TFT_SCLK 14
#define TFT_CS   15  
#define TFT_DC   2   
#define TFT_RST  4   
#define TFT_BL   27  // Backlight control (PWM)

// Touch screen pins (if using)
#define TOUCH_CS 33

// SD Card pins (ESP32-A1S has built-in SD slot)
#define SD_CS 5
#define SD_MISO 12
#define SD_MOSI 13
#define SD_SCK  14

// ES8388 Audio Codec I2S pins
#define PIN_I2S_MCLK 0      // Master clock
#define PIN_I2S_BCK  27     // Bit clock
#define PIN_I2S_WS   25     // Word select (LRCLK)
#define PIN_I2S_DOUT 26     // Data out (to codec)
#define PIN_I2S_DIN  35     // Data in (from codec)

// ES8388 I2C control pins
#define ES8388_I2C_SDA 33
#define ES8388_I2C_SCL 32
#define ES8388_I2C_ADDR 0x10  // ES8388 I2C address

// Board buttons (ESP32-A1S specific)
#define KEY1_PIN 36  // Key 1
#define KEY2_PIN 13  // Key 2  
#define KEY3_PIN 19  // Key 3
#define KEY4_PIN 23  // Key 4
#define KEY5_PIN 18  // Key 5
#define KEY6_PIN 5   // Key 6

// Board LEDs
#define LED_GREEN 22  // Green LED
#define LED_RED   19  // Red LED (may conflict with KEY3)

// Power amplifier control
#define PA_EN_PIN 21  // Power amplifier enable

// Display configuration
#define TFT_WIDTH  240
#define TFT_HEIGHT 320

// Color depth
#define TFT_RGB_ORDER TFT_BGR  // Colour order Blue-Green-Red

// Fonts to be available
#define LOAD_GLCD   // Font 1. Original Adafruit 8 pixel font needs ~1820 bytes in FLASH
#define LOAD_FONT2  // Font 2. Small 16 pixel high font, needs ~3534 bytes in FLASH
#define LOAD_FONT4  // Font 4. Medium 26 pixel high font, needs ~5848 bytes in FLASH
#define LOAD_FONT6  // Font 6. Large 48 pixel high font, needs ~2666 bytes in FLASH
#define LOAD_FONT7  // Font 7. 7 segment 48 pixel high font, needs ~2438 bytes in FLASH
#define LOAD_FONT8  // Font 8. Large 75 pixel high font, needs ~3256 bytes in FLASH
#define LOAD_GFXFF  // FreeFonts. Include access to the 48 Adafruit_GFX free fonts

#define SMOOTH_FONT

// SPI frequency
#define SPI_FREQUENCY       27000000  // 27 MHz
#define SPI_READ_FREQUENCY  20000000  // 20 MHz
#define SPI_TOUCH_FREQUENCY  2500000  // 2.5 MHz

// Optional reduced SPI frequency for stability
// #define SPI_FREQUENCY       20000000
// #define SPI_READ_FREQUENCY  10000000
