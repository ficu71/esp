/**
 * ESP32-A1S Audio Test Example
 * 
 * This example demonstrates basic audio functionality of the ESP32-A1S board:
 * - ES8388 codec initialization
 * - Audio input from microphones
 * - Audio output to speakers
 * - Volume control via buttons
 * - Visual feedback on TFT display
 * 
 * Hardware: ESP32-A1S Audio Board
 * Author: ficu71
 */

#include <Wire.h>
#include <TFT_eSPI.h>
#include <driver/i2s.h>
#include "../../../esp32_marauder/ES8388_init.h"

// Pin definitions for ESP32-A1S
#define BTN_UP    13
#define BTN_DOWN  18
#define BTN_SELECT 5
#define LED_GREEN 22
#define LED_RED   19

// I2S configuration
#define I2S_PORT I2S_NUM_0
#define SAMPLE_RATE 44100
#define BUFFER_SIZE 1024

// Global objects
TFT_eSPI tft = TFT_eSPI();
ES8388 codec;

// Audio buffer
int16_t audioBuffer[BUFFER_SIZE];
size_t bytesRead = 0;
size_t bytesWritten = 0;

// State variables
int volume = 50;
bool isPlaying = false;
unsigned long lastUpdate = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("\nESP32-A1S Audio Test");
  
  // Initialize buttons
  pinMode(BTN_UP, INPUT_PULLUP);
  pinMode(BTN_DOWN, INPUT_PULLUP);
  pinMode(BTN_SELECT, INPUT_PULLUP);
  
  // Initialize LEDs
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);
  
  // Initialize TFT display
  tft.init();
  tft.setRotation(1);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_GREEN, TFT_BLACK);
  tft.setTextSize(2);
  tft.drawString("ESP32-A1S Audio", 10, 10);
  tft.drawString("Test Program", 10, 35);
  tft.setTextSize(1);
  tft.drawString("Initializing codec...", 10, 70);
  
  // Initialize ES8388 codec
  if (!codec.begin(33, 32, 21)) {
    Serial.println("Failed to initialize ES8388!");
    tft.setTextColor(TFT_RED);
    tft.drawString("CODEC INIT FAILED!", 10, 90);
    digitalWrite(LED_RED, HIGH);
    while(1) delay(1000);
  }
  
  tft.setTextColor(TFT_GREEN);
  tft.drawString("Codec initialized OK", 10, 90);
  digitalWrite(LED_GREEN, HIGH);
  
  // Configure I2S
  configureI2S();
  
  tft.drawString("I2S configured", 10, 110);
  
  // Display controls
  tft.setTextColor(TFT_CYAN);
  tft.drawString("Controls:", 10, 140);
  tft.drawString("UP: Volume +", 10, 160);
  tft.drawString("DOWN: Volume -", 10, 180);
  tft.drawString("SELECT: Start/Stop", 10, 200);
  
  updateVolumeDisplay();
  
  Serial.println("Setup complete!");
}

void loop() {
  // Handle button presses
  handleButtons();
  
  // Audio passthrough (microphone to speaker)
  if (isPlaying) {
    // Read from ADC (microphone)
    i2s_read(I2S_PORT, audioBuffer, sizeof(audioBuffer), &bytesRead, portMAX_DELAY);
    
    // Write to DAC (speaker)
    i2s_write(I2S_PORT, audioBuffer, bytesRead, &bytesWritten, portMAX_DELAY);
    
    // Update level meter
    if (millis() - lastUpdate > 50) {
      updateLevelMeter();
      lastUpdate = millis();
    }
  }
  
  delay(1);
}

void configureI2S() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 256,
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0
  };
  
  i2s_pin_config_t pin_config = {
    .mck_io_num = 0,
    .bck_io_num = 27,
    .ws_io_num = 25,
    .data_out_num = 26,
    .data_in_num = 35
  };
  
  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
  i2s_set_clk(I2S_PORT, SAMPLE_RATE, I2S_BITS_PER_SAMPLE_16BIT, I2S_CHANNEL_STEREO);
  
  Serial.println("I2S configured successfully");
}

void handleButtons() {
  static unsigned long lastPress = 0;
  unsigned long now = millis();
  
  if (now - lastPress < 200) return; // Debounce
  
  // Volume up
  if (digitalRead(BTN_UP) == LOW) {
    volume = min(100, volume + 5);
    codec.setVolume(volume);
    updateVolumeDisplay();
    lastPress = now;
    Serial.printf("Volume: %d%%\n", volume);
  }
  
  // Volume down
  if (digitalRead(BTN_DOWN) == LOW) {
    volume = max(0, volume - 5);
    codec.setVolume(volume);
    updateVolumeDisplay();
    lastPress = now;
    Serial.printf("Volume: %d%%\n", volume);
  }
  
  // Start/Stop audio
  if (digitalRead(BTN_SELECT) == LOW) {
    isPlaying = !isPlaying;
    
    if (isPlaying) {
      tft.fillRect(10, 240, 300, 20, TFT_BLACK);
      tft.setTextColor(TFT_GREEN);
      tft.drawString("Status: PLAYING", 10, 240);
      digitalWrite(LED_GREEN, HIGH);
      digitalWrite(LED_RED, LOW);
      Serial.println("Audio started");
    } else {
      tft.fillRect(10, 240, 300, 20, TFT_BLACK);
      tft.setTextColor(TFT_RED);
      tft.drawString("Status: STOPPED", 10, 240);
      digitalWrite(LED_GREEN, LOW);
      digitalWrite(LED_RED, HIGH);
      Serial.println("Audio stopped");
    }
    
    lastPress = now;
    delay(300); // Extra debounce for select
  }
}

void updateVolumeDisplay() {
  tft.fillRect(10, 260, 300, 40, TFT_BLACK);
  tft.setTextColor(TFT_YELLOW);
  tft.setTextSize(2);
  tft.drawString("Volume: " + String(volume) + "%", 10, 260);
  
  // Draw volume bar
  int barWidth = (volume * 280) / 100;
  tft.fillRect(10, 290, barWidth, 20, TFT_GREEN);
  tft.drawRect(10, 290, 280, 20, TFT_WHITE);
  
  tft.setTextSize(1);
}

void updateLevelMeter() {
  // Calculate average audio level
  long sum = 0;
  for (int i = 0; i < BUFFER_SIZE; i++) {
    sum += abs(audioBuffer[i]);
  }
  int avgLevel = sum / BUFFER_SIZE;
  
  // Map to display range (0-100)
  int level = map(avgLevel, 0, 32767, 0, 100);
  level = constrain(level, 0, 100);
  
  // Draw level meter
  int meterHeight = (level * 200) / 100;
  tft.fillRect(290, 70, 20, 200, TFT_BLACK);
  tft.fillRect(290, 270 - meterHeight, 20, meterHeight, TFT_CYAN);
  tft.drawRect(290, 70, 20, 200, TFT_WHITE);
}
