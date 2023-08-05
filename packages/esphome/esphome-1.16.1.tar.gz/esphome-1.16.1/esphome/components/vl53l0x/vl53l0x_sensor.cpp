#include "vl53l0x_sensor.h"
#include "esphome/core/log.h"

/*
 * Most of the code in this integration is based on the VL53L0x library
 * by Pololu (Pololu Corporation), which in turn is based on the VL53L0X
 * API from ST.
 *
 * For more information about licensing, please view the included LICENSE.txt file
 * in the vl53l0x integration directory.
 */

namespace esphome {
namespace vl53l0x {

static const char *TAG = "vl53l0x";

void VL53L0XSensor::dump_config() {
  LOG_SENSOR("", "VL53L0X", this);
  LOG_UPDATE_INTERVAL(this);
  LOG_I2C_DEVICE(this);
}
void VL53L0XSensor::setup() {
  reg(0x89) |= 0x01;
  reg(0x88) = 0x00;

  reg(0x80) = 0x01;
  reg(0xFF) = 0x01;
  reg(0x00) = 0x00;
  stop_variable_ = reg(0x91).get();

  reg(0x00) = 0x01;
  reg(0xFF) = 0x00;
  reg(0x80) = 0x00;
  reg(0x60) |= 0x12;
  if (this->long_range_)
    this->signal_rate_limit_ = 0.1;
  auto rate_value = static_cast<uint16_t>(signal_rate_limit_ * 128);
  write_byte_16(0x44, rate_value);

  reg(0x01) = 0xFF;

  // getSpadInfo()
  reg(0x80) = 0x01;
  reg(0xFF) = 0x01;
  reg(0x00) = 0x00;
  reg(0xFF) = 0x06;
  reg(0x83) |= 0x04;
  reg(0xFF) = 0x07;
  reg(0x81) = 0x01;
  reg(0x80) = 0x01;
  reg(0x94) = 0x6B;
  reg(0x83) = 0x00;

  while (reg(0x83).get() == 0x00)
    yield();

  reg(0x83) = 0x01;
  uint8_t tmp = reg(0x92).get();
  uint8_t spad_count = tmp & 0x7F;
  bool spad_type_is_aperture = tmp & 0x80;

  reg(0x81) = 0x00;
  reg(0xFF) = 0x06;
  reg(0x83) &= ~0x04;
  reg(0xFF) = 0x01;
  reg(0x00) = 0x01;
  reg(0xFF) = 0x00;
  reg(0x80) = 0x00;

  uint8_t ref_spad_map[6];
  this->read_bytes(0xB0, ref_spad_map, 6);

  reg(0xFF) = 0x01;
  reg(0x4F) = 0x00;
  reg(0x4E) = 0x2C;
  reg(0xFF) = 0x00;
  reg(0xB6) = 0xB4;

  uint8_t first_spad_to_enable = spad_type_is_aperture ? 12 : 0;
  uint8_t spads_enabled = 0;
  for (int i = 0; i < 48; i++) {
    uint8_t &val = ref_spad_map[i / 8];
    uint8_t mask = 1 << (i % 8);

    if (i < first_spad_to_enable || spads_enabled == spad_count)
      val &= ~mask;
    else if (val & mask)
      spads_enabled += 1;
  }

  this->write_bytes(0xB0, ref_spad_map, 6);

  reg(0xFF) = 0x01;
  reg(0x00) = 0x00;
  reg(0xFF) = 0x00;
  reg(0x09) = 0x00;
  reg(0x10) = 0x00;
  reg(0x11) = 0x00;
  reg(0x24) = 0x01;
  reg(0x25) = 0xFF;
  reg(0x75) = 0x00;
  reg(0xFF) = 0x01;
  reg(0x4E) = 0x2C;
  reg(0x48) = 0x00;
  reg(0x30) = 0x20;
  reg(0xFF) = 0x00;
  if (this->long_range_) {
    reg(0x30) = 0x07;  // WAS 0x09
  } else {
    reg(0x30) = 0x09;
  }
  reg(0x54) = 0x00;
  reg(0x31) = 0x04;
  reg(0x32) = 0x03;
  reg(0x40) = 0x83;
  reg(0x46) = 0x25;
  reg(0x60) = 0x00;
  reg(0x27) = 0x00;
  reg(0x50) = 0x06;
  reg(0x51) = 0x00;
  reg(0x52) = 0x96;
  reg(0x56) = 0x08;
  if (this->long_range_) {
    reg(0x57) = 0x50;  // was 0x30
  } else {
    reg(0x57) = 0x30;
  }
  reg(0x61) = 0x00;
  reg(0x62) = 0x00;
  reg(0x64) = 0x00;
  reg(0x65) = 0x00;
  reg(0x66) = 0xA0;
  reg(0xFF) = 0x01;
  reg(0x22) = 0x32;
  reg(0x47) = 0x14;
  reg(0x49) = 0xFF;
  reg(0x4A) = 0x00;
  reg(0xFF) = 0x00;
  reg(0x7A) = 0x0A;
  reg(0x7B) = 0x00;
  reg(0x78) = 0x21;
  reg(0xFF) = 0x01;
  reg(0x23) = 0x34;
  reg(0x42) = 0x00;
  reg(0x44) = 0xFF;
  reg(0x45) = 0x26;
  reg(0x46) = 0x05;
  reg(0x40) = 0x40;
  reg(0x0E) = 0x06;
  reg(0x20) = 0x1A;
  reg(0x43) = 0x40;
  reg(0xFF) = 0x00;
  reg(0x34) = 0x03;
  reg(0x35) = 0x44;
  reg(0xFF) = 0x01;
  reg(0x31) = 0x04;
  reg(0x4B) = 0x09;
  reg(0x4C) = 0x05;
  reg(0x4D) = 0x04;
  reg(0xFF) = 0x00;
  reg(0x44) = 0x00;
  reg(0x45) = 0x20;
  reg(0x47) = 0x08;
  if (this->long_range_) {
    reg(0x48) = 0x48;  // was 0x28
  } else {
    reg(0x48) = 0x28;
  }
  reg(0x67) = 0x00;
  reg(0x70) = 0x04;
  reg(0x71) = 0x01;
  reg(0x72) = 0xFE;
  reg(0x76) = 0x00;
  reg(0x77) = 0x00;
  reg(0xFF) = 0x01;
  reg(0x0D) = 0x01;
  reg(0xFF) = 0x00;
  reg(0x80) = 0x01;
  reg(0x01) = 0xF8;
  reg(0xFF) = 0x01;
  reg(0x8E) = 0x01;
  reg(0x00) = 0x01;
  reg(0xFF) = 0x00;
  reg(0x80) = 0x00;

  reg(0x0A) = 0x04;
  reg(0x84) &= ~0x10;
  reg(0x0B) = 0x01;

  measurement_timing_budget_us_ = get_measurement_timing_budget_();
  reg(0x01) = 0xE8;
  set_measurement_timing_budget_(measurement_timing_budget_us_);
  reg(0x01) = 0x01;

  if (!perform_single_ref_calibration_(0x40)) {
    ESP_LOGW(TAG, "1st reference calibration failed!");
    this->mark_failed();
    return;
  }
  reg(0x01) = 0x02;
  if (!perform_single_ref_calibration_(0x00)) {
    ESP_LOGW(TAG, "2nd reference calibration failed!");
    this->mark_failed();
    return;
  }
  reg(0x01) = 0xE8;
}
void VL53L0XSensor::update() {
  if (this->initiated_read_ || this->waiting_for_interrupt_) {
    this->publish_state(NAN);
    this->status_set_warning();
  }

  // initiate single shot measurement
  reg(0x80) = 0x01;
  reg(0xFF) = 0x01;

  reg(0x00) = 0x00;
  reg(0x91) = stop_variable_;
  reg(0x00) = 0x01;
  reg(0xFF) = 0x00;
  reg(0x80) = 0x00;

  reg(0x00) = 0x01;
  this->waiting_for_interrupt_ = false;
  this->initiated_read_ = true;
  // wait for timeout
}
void VL53L0XSensor::loop() {
  if (this->initiated_read_) {
    if (reg(0x00).get() & 0x01) {
      // waiting
    } else {
      // done
      // wait until reg(0x13) & 0x07 is set
      this->initiated_read_ = false;
      this->waiting_for_interrupt_ = true;
    }
  }
  if (this->waiting_for_interrupt_) {
    if (reg(0x13).get() & 0x07) {
      uint16_t range_mm;
      this->read_byte_16(0x14 + 10, &range_mm);
      reg(0x0B) = 0x01;
      this->waiting_for_interrupt_ = false;

      if (range_mm >= 8190) {
        ESP_LOGW(TAG, "'%s' - Distance is out of range, please move the target closer", this->name_.c_str());
        this->publish_state(NAN);
        return;
      }

      float range_m = range_mm / 1e3f;
      ESP_LOGD(TAG, "'%s' - Got distance %.3f m", this->name_.c_str(), range_m);
      this->publish_state(range_m);
    }
  }
}

}  // namespace vl53l0x
}  // namespace esphome
