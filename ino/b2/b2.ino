/*
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
*/

#include "Timer.h"
Timer t;

const int analog_pin = 5; // pin number to be sampled
int led_id;
bool led_blinking = false;

void setup() {
  Serial.begin(9600);
  pinMode(analog_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  t.update();
  if(Serial.available() > 0) {
    int command = Serial.parseInt();
    switch(command) {
      case 0: { // stop acquisition
        if (led_blinking == true) {
          t.stop(led_id);
          led_blinking = false;
        }
        break;
      }
      case 1: { // start acquisition
        if (led_blinking == false) {
            led_id = t.oscillate(LED_BUILTIN, 500, HIGH);
            led_blinking = true;
          }
        Serial.println(analogRead(analog_pin));
        digitalWrite(LED_BUILTIN, LOW);
        break;
      }
    }
  }
}
