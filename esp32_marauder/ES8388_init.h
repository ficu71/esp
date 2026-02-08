/**
 * ES8388 Audio Codec Initialization for ESP32-A1S
 * 
 * This library provides initialization and control functions for the
 * ES8388 audio codec found on ESP32-A1S boards.
 * 
 * Author: ficu71
 * Based on: AI-Thinker ESP32-A1S documentation
 */

#ifndef ES8388_INIT_H
#define ES8388_INIT_H

#include <Arduino.h>
#include <Wire.h>

// ES8388 I2C Address
#define ES8388_ADDR 0x10

// ES8388 Register Map
#define ES8388_CONTROL1         0x00
#define ES8388_CONTROL2         0x01
#define ES8388_CHIPPOWER        0x02
#define ES8388_ADCPOWER         0x03
#define ES8388_DACPOWER         0x04
#define ES8388_CHIPLOPOW1       0x05
#define ES8388_CHIPLOPOW2       0x06
#define ES8388_ANAVOLMANAG      0x07
#define ES8388_MASTERMODE       0x08
#define ES8388_ADCCONTROL1      0x09
#define ES8388_ADCCONTROL2      0x0A
#define ES8388_ADCCONTROL3      0x0B
#define ES8388_ADCCONTROL4      0x0C
#define ES8388_ADCCONTROL5      0x0D
#define ES8388_ADCCONTROL6      0x0E
#define ES8388_ADCCONTROL7      0x0F
#define ES8388_ADCCONTROL8      0x10
#define ES8388_ADCCONTROL9      0x11
#define ES8388_ADCCONTROL10     0x12
#define ES8388_ADCCONTROL11     0x13
#define ES8388_ADCCONTROL12     0x14
#define ES8388_ADCCONTROL13     0x15
#define ES8388_ADCCONTROL14     0x16
#define ES8388_DACCONTROL1      0x17
#define ES8388_DACCONTROL2      0x18
#define ES8388_DACCONTROL3      0x19
#define ES8388_DACCONTROL4      0x1A
#define ES8388_DACCONTROL5      0x1B
#define ES8388_DACCONTROL6      0x1C
#define ES8388_DACCONTROL7      0x1D
#define ES8388_DACCONTROL8      0x1E
#define ES8388_DACCONTROL9      0x1F
#define ES8388_DACCONTROL10     0x20
#define ES8388_DACCONTROL11     0x21
#define ES8388_DACCONTROL12     0x22
#define ES8388_DACCONTROL13     0x23
#define ES8388_DACCONTROL14     0x24
#define ES8388_DACCONTROL15     0x25
#define ES8388_DACCONTROL16     0x26
#define ES8388_DACCONTROL17     0x27
#define ES8388_DACCONTROL18     0x28
#define ES8388_DACCONTROL19     0x29
#define ES8388_DACCONTROL20     0x2A
#define ES8388_DACCONTROL21     0x2B
#define ES8388_DACCONTROL22     0x2C
#define ES8388_DACCONTROL23     0x2D
#define ES8388_DACCONTROL24     0x2E
#define ES8388_DACCONTROL25     0x2F
#define ES8388_DACCONTROL26     0x30
#define ES8388_DACCONTROL27     0x31
#define ES8388_DACCONTROL28     0x32
#define ES8388_DACCONTROL29     0x33
#define ES8388_DACCONTROL30     0x34

class ES8388 {
public:
    /**
     * Initialize ES8388 codec
     * @param sda_pin I2C SDA pin
     * @param scl_pin I2C SCL pin
     * @param pa_pin Power amplifier enable pin
     * @return true if initialization successful
     */
    bool begin(uint8_t sda_pin = 33, uint8_t scl_pin = 32, int8_t pa_pin = 21) {
        _pa_pin = pa_pin;
        
        // Initialize I2C
        Wire.begin(sda_pin, scl_pin);
        Wire.setClock(100000); // 100kHz
        
        // Enable power amplifier
        if (_pa_pin >= 0) {
            pinMode(_pa_pin, OUTPUT);
            digitalWrite(_pa_pin, HIGH);
        }
        
        delay(50);
        
        // Check if ES8388 is present
        if (!isPresent()) {
            Serial.println("ES8388 not found!");
            return false;
        }
        
        Serial.println("ES8388 found, initializing...");
        
        // Reset ES8388
        writeReg(ES8388_CONTROL1, 0x80);
        writeReg(ES8388_CONTROL1, 0x00);
        delay(100);
        
        // Power up sequence
        writeReg(ES8388_CHIPPOWER, 0x00);      // Power up
        writeReg(ES8388_MASTERMODE, 0x00);     // Slave mode
        
        // ADC configuration
        writeReg(ES8388_ADCPOWER, 0x00);       // ADC power on
        writeReg(ES8388_ADCCONTROL1, 0x88);    // Mic PGA = +24dB
        writeReg(ES8388_ADCCONTROL2, 0x50);    // Input = MIC1
        writeReg(ES8388_ADCCONTROL3, 0x02);    // ADC format = I2S
        writeReg(ES8388_ADCCONTROL4, 0x0C);    // LRCK/BCK = 256
        writeReg(ES8388_ADCCONTROL5, 0x02);    // ADC FSR = 44.1kHz
        writeReg(ES8388_ADCCONTROL8, 0x00);    // ADC volume = 0dB
        writeReg(ES8388_ADCCONTROL9, 0x00);    // ADC volume = 0dB
        
        // DAC configuration  
        writeReg(ES8388_DACPOWER, 0x00);       // DAC power on
        writeReg(ES8388_DACCONTROL1, 0x18);    // DAC format = I2S
        writeReg(ES8388_DACCONTROL2, 0x02);    // DAC FSR = 44.1kHz
        writeReg(ES8388_DACCONTROL3, 0x00);    // LRCK/BCK = 256
        writeReg(ES8388_DACCONTROL4, 0x00);    // LOUT2/ROUT2 volume = 0dB
        writeReg(ES8388_DACCONTROL5, 0x00);    // LOUT2/ROUT2 volume = 0dB
        writeReg(ES8388_DACCONTROL16, 0x00);   // 0dB
        writeReg(ES8388_DACCONTROL17, 0x90);   // Automute off
        writeReg(ES8388_DACCONTROL20, 0x90);   // Automute off
        writeReg(ES8388_DACCONTROL21, 0xA0);   // DAC output
        writeReg(ES8388_DACCONTROL22, 0xA0);   // DAC output
        writeReg(ES8388_DACCONTROL23, 0x00);   // DAC volume = 0dB
        writeReg(ES8388_DACCONTROL24, 0x00);   // DAC volume = 0dB
        writeReg(ES8388_DACCONTROL25, 0x00);   // DAC volume = 0dB
        
        // Set initial volume
        setVolume(50); // 50% volume
        
        Serial.println("ES8388 initialized successfully!");
        return true;
    }
    
    /**
     * Check if ES8388 is present on I2C bus
     */
    bool isPresent() {
        Wire.beginTransmission(ES8388_ADDR);
        return (Wire.endTransmission() == 0);
    }
    
    /**
     * Set output volume (0-100)
     */
    void setVolume(uint8_t volume) {
        if (volume > 100) volume = 100;
        
        // Convert 0-100 to 0-33 (ES8388 volume range)
        uint8_t vol = (volume * 33) / 100;
        
        // Invert value (ES8388 uses attenuation)
        vol = 33 - vol;
        
        writeReg(ES8388_DACCONTROL24, vol); // Left channel
        writeReg(ES8388_DACCONTROL25, vol); // Right channel
        
        _volume = volume;
    }
    
    /**
     * Get current volume
     */
    uint8_t getVolume() {
        return _volume;
    }
    
    /**
     * Mute/unmute output
     */
    void mute(bool enable) {
        if (enable) {
            writeReg(ES8388_DACCONTROL3, 0x04); // Mute
        } else {
            writeReg(ES8388_DACCONTROL3, 0x00); // Unmute
        }
    }
    
    /**
     * Enable/disable power amplifier
     */
    void powerAmplifier(bool enable) {
        if (_pa_pin >= 0) {
            digitalWrite(_pa_pin, enable ? HIGH : LOW);
        }
    }
    
    /**
     * Set microphone gain (0-8, 0=0dB, 8=+24dB)
     */
    void setMicGain(uint8_t gain) {
        if (gain > 8) gain = 8;
        uint8_t val = gain << 4;
        writeReg(ES8388_ADCCONTROL1, val | val); // Both channels
    }
    
    /**
     * Power down codec
     */
    void powerDown() {
        writeReg(ES8388_DACPOWER, 0xFF);    // DAC off
        writeReg(ES8388_ADCPOWER, 0xFF);    // ADC off
        writeReg(ES8388_CHIPPOWER, 0xFF);   // Chip off
        
        if (_pa_pin >= 0) {
            digitalWrite(_pa_pin, LOW);      // PA off
        }
    }

private:
    int8_t _pa_pin = -1;
    uint8_t _volume = 50;
    
    /**
     * Write to ES8388 register
     */
    void writeReg(uint8_t reg, uint8_t val) {
        Wire.beginTransmission(ES8388_ADDR);
        Wire.write(reg);
        Wire.write(val);
        Wire.endTransmission();
    }
    
    /**
     * Read from ES8388 register
     */
    uint8_t readReg(uint8_t reg) {
        Wire.beginTransmission(ES8388_ADDR);
        Wire.write(reg);
        Wire.endTransmission(false);
        
        Wire.requestFrom((uint8_t)ES8388_ADDR, (uint8_t)1);
        return Wire.read();
    }
};

#endif // ES8388_INIT_H
