#pragma once

#ifndef configs_h

  #define configs_h

  #define POLISH_POTATO

  //#define DEVELOPER

  //// BOARD TARGETS
  //#define MARAUDER_M5STICKC
  //#define MARAUDER_M5STICKCP2
  //#define MARAUDER_MINI
  //#define MARAUDER_V4
  //#define MARAUDER_V6
  //#define MARAUDER_V6_1
  //#define MARAUDER_V7
  //#define MARAUDER_V7_1
  //#define MARAUDER_KIT
  //#define GENERIC_ESP32
  //#define MARAUDER_FLIPPER
  //#define MARAUDER_MULTIBOARD_S3
  //#define ESP32_LDDB
  //#define MARAUDER_DEV_BOARD_PRO
  //#define XIAO_ESP32_S3
  //#define MARAUDER_REV_FEATHER
  //#define MARAUDER_CYD_MICRO // 2432S028
  //#define MARAUDER_CYD_2USB // Another 2432S028 but it has tWo UsBs OoOoOoO
  //#define MARAUDER_CYD_GUITION // ESP32-2432S024 GUITION
  //#define MARAUDER_CYD_3_5_INCH
  //#define MARAUDER_C5
  //#define MARAUDER_CARDPUTER
  //#define MARAUDER_V8
  //#define MARAUDER_MINI_V3
  //#define ESP32_A1S  // ESP32-A1S Audio Board with ES8388 codec
  //// END BOARD TARGETS

  #define MARAUDER_VERSION "v1.10.2"

  #define GRAPH_REFRESH   100

  #define TRACK_EVICT_SEC 90 // Seconds before marking tracked MAC as tombstone

  #define DUAL_BAND_CHANNELS 51

  #define DISPLAY_BUFFER_LIMIT 20

  //// HARDWARE NAMES
  #ifdef MARAUDER_M5STICKC
    #define HARDWARE_NAME "M5Stick-C Plus"
  #elif defined(MARAUDER_M5STICKCP2)
    #define HARDWARE_NAME "M5Stick-C Plus2"
  #elif defined(MARAUDER_CARDPUTER)
    #define HARDWARE_NAME "M5 Cardputer"
  #elif defined(MARAUDER_MINI)
    #define HARDWARE_NAME "Marauder Mini"
  #elif defined(MARAUDER_V7)
    #define HARDWARE_NAME "Marauder v7"
  #elif defined(MARAUDER_V7_1)
    #define HARDWARE_NAME "Marauder v7.1"
  #elif defined(MARAUDER_REV_FEATHER)
    #define HARDWARE_NAME "Adafruit Feather ESP32-S2 Reverse TFT"
  #elif defined(MARAUDER_V4)
    #define HARDWARE_NAME "Marauder v4"
  #elif defined(MARAUDER_V6)
    #define HARDWARE_NAME "Marauder v6"
  #elif defined(MARAUDER_V6_1)
    #define HARDWARE_NAME "Marauder v6.1"
  #elif defined(MARAUDER_CYD_MICRO)
    #define HARDWARE_NAME "CYD 2432S028"
  #elif defined(MARAUDER_CYD_2USB)
    #define HARDWARE_NAME "CYD 2432S028 2USB"
  #elif defined(MARAUDER_CYD_3_5_INCH)
    #define HARDWARE_NAME "CYD 3.5inch"
  #elif defined(MARAUDER_CYD_GUITION)
    #define HARDWARE_NAME "CYD 2432S024 GUITION"
  #elif defined(MARAUDER_KIT)
    #define HARDWARE_NAME "Marauder Kit"
  #elif defined(MARAUDER_FLIPPER)
    #define HARDWARE_NAME "Flipper Zero Dev Board"
  #elif defined(MARAUDER_MULTIBOARD_S3)
    #define HARDWARE_NAME "Flipper Zero Multi Board S3"
  #elif defined(ESP32_LDDB)
    #define HARDWARE_NAME "ESP32 LDDB"
  #elif defined(MARAUDER_DEV_BOARD_PRO)
    #define HARDWARE_NAME "Flipper Zero Dev Board Pro"
  #elif defined(XIAO_ESP32_S3)
    #define HARDWARE_NAME "XIAO ESP32 S3"
  #elif defined(MARAUDER_C5)
    #define HARDWARE_NAME "ESP32-C5 DevKit"
  #elif defined(MARAUDER_V8)
    #define HARDWARE_NAME "Marauder v8"
  #elif defined(MARAUDER_MINI_V3)
    #define HARDWARE_NAME "Marauder Mini v3"
  #elif defined(ESP32_A1S)
    #define HARDWARE_NAME "ESP32-A1S Audio Board"
  #else
    #define HARDWARE_NAME "ESP32"
  #endif

  //// END HARDWARE NAMES