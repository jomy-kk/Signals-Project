/*
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
*/

#include "Timer.h"
Timer t;

const int sampling_frequency = 400; // Hz
const int analog_pin = 5; // pin number to be sampled
int led_id;
bool led_blinking = false;
volatile int acquire = 0;

void setup() {
  Serial.begin(19200);
  pinMode(analog_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  t.update();
  // Update acquire status
  if(Serial.available() > 0) {
    int command = Serial.parseInt();
    switch(command) {
      case 0: { // stop acquisition
        if (led_blinking == true) {
          t.stop(led_id);
          led_blinking = false;
        }
        Serial.println("stop");
        acquire = 0;
        break;
      }
      case 1: { // start acquisition
        if (led_blinking == false) {
            led_id = t.oscillate(LED_BUILTIN, 500, HIGH);
            led_blinking = true;
          }
        acquire = 1;
        break;
      }
    }
  }

  // Acquire a sample?
  if(acquire) {
    Serial.println(String(millis()) + ':' + String(analogRead(analog_pin)));
    // Serial.read(); // uncomment to test ad-hoc
  }

  delay(1/sampling_frequency*1000);
}
