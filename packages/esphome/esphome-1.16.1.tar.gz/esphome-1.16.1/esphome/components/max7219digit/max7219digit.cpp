#include "max7219digit.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"
#include "max7219font.h"

namespace esphome {
namespace max7219digit {

static const char *TAG = "max7219DIGIT";

static const uint8_t MAX7219_REGISTER_NOOP = 0x00;
static const uint8_t MAX7219_REGISTER_DECODE_MODE = 0x09;
static const uint8_t MAX7219_REGISTER_INTENSITY = 0x0A;
static const uint8_t MAX7219_REGISTER_SCAN_LIMIT = 0x0B;
static const uint8_t MAX7219_REGISTER_SHUTDOWN = 0x0C;
static const uint8_t MAX7219_REGISTER_DISPLAY_TEST = 0x0F;
constexpr uint8_t MAX7219_NO_SHUTDOWN = 0x00;
constexpr uint8_t MAX7219_SHUTDOWN = 0x01;
constexpr uint8_t MAX7219_NO_DISPLAY_TEST = 0x00;
constexpr uint8_t MAX7219_DISPLAY_TEST = 0x01;

float MAX7219Component::get_setup_priority() const { return setup_priority::PROCESSOR; }

void MAX7219Component::setup() {
  ESP_LOGCONFIG(TAG, "Setting up MAX7219_DIGITS...");
  this->spi_setup();
  this->stepsleft_ = 0;
  this->max_displaybuffer_.reserve(500);  // Create base space to write buffer
  // Initialize buffer with 0 for display so all non written pixels are blank
  this->max_displaybuffer_.resize(this->num_chips_ * 8, 0);
  // let's assume the user has all 8 digits connected, only important in daisy chained setups anyway
  this->send_to_all_(MAX7219_REGISTER_SCAN_LIMIT, 7);
  // let's use our own ASCII -> led pattern encoding
  this->send_to_all_(MAX7219_REGISTER_DECODE_MODE, 0);
  // No display test with all the pixels on
  this->send_to_all_(MAX7219_REGISTER_DISPLAY_TEST, MAX7219_NO_DISPLAY_TEST);
  // SET Intsity of display
  this->send_to_all_(MAX7219_REGISTER_INTENSITY, this->intensity_);
  // this->send_to_all_(MAX7219_REGISTER_INTENSITY, 1);
  this->display();
  // power up
  this->send_to_all_(MAX7219_REGISTER_SHUTDOWN, 1);
}

void MAX7219Component::dump_config() {
  ESP_LOGCONFIG(TAG, "MAX7219DIGIT:");
  ESP_LOGCONFIG(TAG, "  Number of Chips: %u", this->num_chips_);
  ESP_LOGCONFIG(TAG, "  Intensity: %u", this->intensity_);
  ESP_LOGCONFIG(TAG, "  Scroll Mode: %u", this->scroll_mode_);
  ESP_LOGCONFIG(TAG, "  Scroll Speed: %u", this->scroll_speed_);
  ESP_LOGCONFIG(TAG, "  Scroll Dwell: %u", this->scroll_dwell_);
  ESP_LOGCONFIG(TAG, "  Scroll Delay: %u", this->scroll_delay_);
  LOG_PIN("  CS Pin: ", this->cs_);
  LOG_UPDATE_INTERVAL(this);
}

void MAX7219Component::loop() {
  unsigned long now = millis();

  // check if the buffer has shrunk past the current position since last update
  if ((this->max_displaybuffer_.size() >= this->old_buffer_size_ + 3) ||
      (this->max_displaybuffer_.size() <= this->old_buffer_size_ - 3)) {
    this->stepsleft_ = 0;
    this->display();
    this->old_buffer_size_ = this->max_displaybuffer_.size();
  }

  // Reset the counter back to 0 when full string has been displayed.
  if (this->stepsleft_ > this->max_displaybuffer_.size())
    this->stepsleft_ = 0;

  // Return if there is no need to scroll or scroll is off
  if (!this->scroll_ || (this->max_displaybuffer_.size() <= this->num_chips_ * 8)) {
    this->display();
    return;
  }

  if ((this->stepsleft_ == 0) && (now - this->last_scroll_ < this->scroll_delay_)) {
    this->display();
    return;
  }

  // Dwell time at end of string in case of stop at end
  if (this->scroll_mode_ == 1) {
    if (this->stepsleft_ >= this->max_displaybuffer_.size() - this->num_chips_ * 8 + 1) {
      if (now - this->last_scroll_ >= this->scroll_dwell_) {
        this->stepsleft_ = 0;
        this->last_scroll_ = now;
        this->display();
      }
      return;
    }
  }

  // Actual call to scroll left action
  if (now - this->last_scroll_ >= this->scroll_speed_) {
    this->last_scroll_ = now;
    this->scroll_left();
    this->display();
  }
}

void MAX7219Component::display() {
  uint8_t pixels[8];
  // Run this loop for every MAX CHIP (GRID OF 64 leds)
  // Run this routine for the rows of every chip 8x row 0 top to 7 bottom
  // Fill the pixel parameter with diplay data
  // Send the data to the chip
  for (uint8_t i = 0; i < this->num_chips_; i++) {
    for (uint8_t j = 0; j < 8; j++) {
      if (this->reverse_) {
        pixels[j] = this->max_displaybuffer_[(this->num_chips_ - i - 1) * 8 + j];
      } else {
        pixels[j] = this->max_displaybuffer_[i * 8 + j];
      }
    }
    this->send64pixels(i, pixels);
  }
}

int MAX7219Component::get_height_internal() {
  return 8;  // TO BE DONE -> STACK TWO DISPLAYS ON TOP OF EACH OTHE
             // TO BE DONE -> CREATE Virtual size of screen and scroll
}

int MAX7219Component::get_width_internal() { return this->num_chips_ * 8; }

size_t MAX7219Component::get_buffer_length_() { return this->num_chips_ * 8; }

void HOT MAX7219Component::draw_absolute_pixel_internal(int x, int y, Color color) {
  if (x + 1 > this->max_displaybuffer_.size()) {  // Extend the display buffer in case required
    this->max_displaybuffer_.resize(x + 1, this->bckgrnd_);
  }

  if ((y >= this->get_height_internal()) || (y < 0) || (x < 0))  // If pixel is outside display then dont draw
    return;

  uint16_t pos = x;    // X is starting at 0 top left
  uint8_t subpos = y;  // Y is starting at 0 top left

  if (color.is_on()) {
    this->max_displaybuffer_[pos] |= (1 << subpos);
  } else {
    this->max_displaybuffer_[pos] &= ~(1 << subpos);
  }
}

void MAX7219Component::send_byte_(uint8_t a_register, uint8_t data) {
  this->write_byte(a_register);  // Write register value to MAX
  this->write_byte(data);        // Followed by actual data
}
void MAX7219Component::send_to_all_(uint8_t a_register, uint8_t data) {
  this->enable();                                 // Enable SPI
  for (uint8_t i = 0; i < this->num_chips_; i++)  // Run the loop for every MAX chip in the stack
    this->send_byte_(a_register, data);           // Send the data to the chips
  this->disable();                                // Disable SPI
}
void MAX7219Component::update() {
  this->update_ = true;
  this->max_displaybuffer_.clear();
  this->max_displaybuffer_.resize(this->num_chips_ * 8, this->bckgrnd_);
  if (this->writer_local_.has_value())  // insert Labda function if available
    (*this->writer_local_)(*this);
}

void MAX7219Component::invert_on_off(bool on_off) { this->invert_ = on_off; };
void MAX7219Component::invert_on_off() { this->invert_ = !this->invert_; };

void MAX7219Component::turn_on_off(bool on_off) {
  if (on_off) {
    this->send_to_all_(MAX7219_REGISTER_SHUTDOWN, 1);
  } else {
    this->send_to_all_(MAX7219_REGISTER_SHUTDOWN, 0);
  }
}

void MAX7219Component::scroll(bool on_off, uint8_t mode, uint16_t speed, uint16_t delay, uint16_t dwell) {
  this->set_scroll(on_off);
  this->set_scroll_mode(mode);
  this->set_scroll_speed(speed);
  this->set_scroll_dwell(dwell);
  this->set_scroll_delay(delay);
}

void MAX7219Component::scroll(bool on_off, uint8_t mode) {
  this->set_scroll(on_off);
  this->set_scroll_mode(mode);
}

void MAX7219Component::intensity(uint8_t intensity) {
  this->intensity_ = intensity;
  this->send_to_all_(MAX7219_REGISTER_INTENSITY, this->intensity_);
}

void MAX7219Component::scroll(bool on_off) { this->set_scroll(on_off); }

void MAX7219Component::scroll_left() {
  if (this->update_) {
    this->max_displaybuffer_.push_back(this->bckgrnd_);
    for (uint16_t i = 0; i < this->stepsleft_; i++) {
      this->max_displaybuffer_.push_back(this->max_displaybuffer_.front());
      this->max_displaybuffer_.erase(this->max_displaybuffer_.begin());
      this->update_ = false;
    }
  } else {
    this->max_displaybuffer_.push_back(this->max_displaybuffer_.front());
    this->max_displaybuffer_.erase(this->max_displaybuffer_.begin());
  }
  this->stepsleft_++;
}

void MAX7219Component::send_char(uint8_t chip, uint8_t data) {
  // get this character from PROGMEM
  for (uint8_t i = 0; i < 8; i++)
    this->max_displaybuffer_[chip * 8 + i] = pgm_read_byte(&MAX7219_DOT_MATRIX_FONT[data][i]);
}  // end of send_char

// send one character (data) to position (chip)

void MAX7219Component::send64pixels(uint8_t chip, const uint8_t pixels[8]) {
  for (uint8_t col = 0; col < 8; col++) {  // RUN THIS LOOP 8 times until column is 7
    this->enable();                        // start sending by enabling SPI
    for (uint8_t i = 0; i < chip; i++)     // send extra NOPs to push the pixels out to extra displays
      this->send_byte_(MAX7219_REGISTER_NOOP,
                       MAX7219_REGISTER_NOOP);  // run this loop unit the matching chip is reached
    uint8_t b = 0;                              // rotate pixels 90 degrees -- set byte to 0
    if (this->orientation_ == 0) {
      for (uint8_t i = 0; i < 8; i++) {
        // run this loop 8 times for all the pixels[8] received
        b |= ((pixels[i] >> col) & 1) << (7 - i);  // change the column bits into row bits
      }
    } else if (this->orientation_ == 1) {
      b = pixels[col];
    } else if (this->orientation_ == 2) {
      for (uint8_t i = 0; i < 8; i++) {
        b |= ((pixels[i] >> (7 - col)) & 1) << i;
      }
    } else {
      b = pixels[7 - col];
    }
    // send this byte to dispay at selected chip
    if (this->invert_) {
      this->send_byte_(col + 1, ~b);
    } else {
      this->send_byte_(col + 1, b);
    }
    for (int i = 0; i < this->num_chips_ - chip - 1; i++)  // end with enough NOPs so later chips don't update
      this->send_byte_(MAX7219_REGISTER_NOOP, MAX7219_REGISTER_NOOP);
    this->disable();  // all done disable SPI
  }                   // end of for each column
}  // end of send64pixels

uint8_t MAX7219Component::printdigit(const char *str) { return this->printdigit(0, str); }

uint8_t MAX7219Component::printdigit(uint8_t start_pos, const char *s) {
  uint8_t chip = start_pos;
  for (; chip < this->num_chips_ && *s; chip++)
    send_char(chip, *s++);
  // space out rest
  while (chip < (this->num_chips_))
    send_char(chip++, ' ');
  return 0;
}  // end of sendString

uint8_t MAX7219Component::printdigitf(uint8_t pos, const char *format, ...) {
  va_list arg;
  va_start(arg, format);
  char buffer[64];
  int ret = vsnprintf(buffer, sizeof(buffer), format, arg);
  va_end(arg);
  if (ret > 0)
    return this->printdigit(pos, buffer);
  return 0;
}
uint8_t MAX7219Component::printdigitf(const char *format, ...) {
  va_list arg;
  va_start(arg, format);
  char buffer[64];
  int ret = vsnprintf(buffer, sizeof(buffer), format, arg);
  va_end(arg);
  if (ret > 0)
    return this->printdigit(buffer);
  return 0;
}

#ifdef USE_TIME
uint8_t MAX7219Component::strftimedigit(uint8_t pos, const char *format, time::ESPTime time) {
  char buffer[64];
  size_t ret = time.strftime(buffer, sizeof(buffer), format);
  if (ret > 0)
    return this->printdigit(pos, buffer);
  return 0;
}
uint8_t MAX7219Component::strftimedigit(const char *format, time::ESPTime time) {
  return this->strftimedigit(0, format, time);
}
#endif

}  // namespace max7219digit
}  // namespace esphome
