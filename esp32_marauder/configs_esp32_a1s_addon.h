// ##################################################################################
// ESP32-A1S COMPLETE HARDWARE CONFIGURATION
// Add this section to your main configs.h file after the existing board configurations
// ##################################################################################

// BOARD FEATURES for ESP32-A1S
#ifdef ESP32_A1S
  //#define FLIPPER_ZERO_HAT
  //#define HAS_BATTERY  // Can be added if using external battery
  #define HAS_BT
  #define HAS_BUTTONS
  //#define HAS_NEOPIXEL_LED
  //#define HAS_PWR_MGMT
  #define HAS_SCREEN
  #define HAS_FULL_SCREEN
  #define HAS_SD
  #define USE_SD
  #define HAS_TEMP_SENSOR
  #define HAS_GPS
  #define HAS_AUDIO_CODEC  // ESP32-A1S specific feature
  #define HAS_I2S_AUDIO    // ESP32-A1S specific feature
#endif

// BUTTON DEFINITIONS for ESP32-A1S
#ifdef ESP32_A1S
  #define L_BTN 36   // KEY1
  #define C_BTN 5    // KEY6 (center/select)
  #define U_BTN 13   // KEY2 (up)
  #define R_BTN 23   // KEY4 (right)
  #define D_BTN 18   // KEY5 (down)

  #define HAS_L
  #define HAS_R
  #define HAS_U
  #define HAS_D
  #define HAS_C

  #define L_PULL true
  #define C_PULL true
  #define U_PULL true
  #define R_PULL true
  #define D_PULL true
#endif

// DISPLAY DEFINITIONS for ESP32-A1S
#ifdef ESP32_A1S
  #define CHAN_PER_PAGE 7

  #define SCREEN_CHAR_WIDTH 40
  #define HAS_ILI9341
  
  #define BANNER_TEXT_SIZE 2

  #ifndef TFT_WIDTH
    #define TFT_WIDTH 240
  #endif

  #ifndef TFT_HEIGHT
    #define TFT_HEIGHT 320
  #endif

  #define TFT_MISO 12
  #define TFT_MOSI 13
  #define TFT_SCLK 14
  #define TFT_CS   15
  #define TFT_DC   2
  #define TFT_RST  4
  #define TFT_BL   27  // Backlight PWM control
  #define TOUCH_CS 33

  #define GRAPH_VERT_LIM TFT_HEIGHT/2 - 1

  #define EXT_BUTTON_WIDTH 20

  #define SCREEN_BUFFER

  #define MAX_SCREEN_BUFFER 22

  #define SCREEN_ORIENTATION 0
  
  #define CHAR_WIDTH 12
  #define SCREEN_WIDTH TFT_WIDTH
  #define SCREEN_HEIGHT TFT_HEIGHT
  #define HEIGHT_1 TFT_WIDTH
  #define WIDTH_1 TFT_HEIGHT
  #define STANDARD_FONT_CHAR_LIMIT (TFT_WIDTH/6)
  #define TEXT_HEIGHT 16
  #define BOT_FIXED_AREA 0
  #define TOP_FIXED_AREA 48
  #define YMAX 320
  #define minimum(a,b)     (((a) < (b)) ? (a) : (b))
  #define MENU_FONT &FreeMono9pt7b
  #define BUTTON_SCREEN_LIMIT 12
  #define BUTTON_ARRAY_LEN BUTTON_SCREEN_LIMIT
  #define STATUS_BAR_WIDTH 16
  #define LVGL_TICK_PERIOD 6

  #define FRAME_X 100
  #define FRAME_Y 64
  #define FRAME_W 120
  #define FRAME_H 50
  
  #define REDBUTTON_X FRAME_X
  #define REDBUTTON_Y FRAME_Y
  #define REDBUTTON_W (FRAME_W/2)
  #define REDBUTTON_H FRAME_H
  
  #define GREENBUTTON_X (REDBUTTON_X + REDBUTTON_W)
  #define GREENBUTTON_Y FRAME_Y
  #define GREENBUTTON_W (FRAME_W/2)
  #define GREENBUTTON_H FRAME_H
  
  #define STATUSBAR_COLOR 0x4A49
  
  #define KIT_LED_BUILTIN 22  // Green LED
#endif

// MENU DEFINITIONS for ESP32-A1S
#ifdef ESP32_A1S
  #define BANNER_TIME 100
  
  #define COMMAND_PREFIX "!"
  
  #define KEY_X 120
  #define KEY_Y 50
  #define KEY_W 240
  #define KEY_H 22
  #define KEY_SPACING_X 0
  #define KEY_SPACING_Y 1
  #define KEY_TEXTSIZE 1
  #define ICON_W 22
  #define ICON_H 22
  #define BUTTON_PADDING 22
#endif

// SD CARD DEFINITIONS for ESP32-A1S
#ifdef ESP32_A1S
  #define SD_CS 5
  #define SD_MISO 12
  #define SD_MOSI 13
  #define SD_SCK  14
#endif

// GPS DEFINITIONS for ESP32-A1S
#ifdef ESP32_A1S
  #define GPS_SERIAL_INDEX 2
  #define GPS_TX 17  // Available GPIO
  #define GPS_RX 16  // Available GPIO
#endif

// AUDIO CODEC DEFINITIONS for ESP32-A1S (ES8388)
#ifdef ESP32_A1S
  // I2S pins for ES8388 audio codec
  #define PIN_I2S_MCLK 0
  #define PIN_I2S_BCK  27
  #define PIN_I2S_WS   25
  #define PIN_I2S_DOUT 26
  #define PIN_I2S_DIN  35
  
  // I2C pins for ES8388 control
  #define ES8388_I2C_SDA 33
  #define ES8388_I2C_SCL 32
  #define ES8388_I2C_ADDR 0x10
  
  // Power amplifier enable
  #define PA_EN_PIN 21
  
  // Audio codec LEDs
  #define AUDIO_LED_GREEN 22
  #define AUDIO_LED_RED   19
#endif

// MEMORY LOWER LIMIT for ESP32-A1S
#ifdef ESP32_A1S
  #define MEM_LOWER_LIM 10000
#endif

// LED DEFINITIONS for ESP32-A1S
#ifdef ESP32_A1S
  // Board has built-in LEDs for audio status
  #define LED_GREEN 22
  #define LED_RED   19
#endif

// ##################################################################################
// USAGE INSTRUCTIONS:
// 1. Copy the above sections and insert them into your main configs.h file
// 2. Place them after the existing board configurations (after MARAUDER_MINI_V3)
// 3. Uncomment #define ESP32_A1S in the BOARD TARGETS section to enable
// 4. Compile and flash to your ESP32-A1S board
// ##################################################################################
