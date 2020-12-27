/*
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
*/

#include "Timer.h"
Timer t;

const float sampling_frequency = 200; // Hz
const int analog_pin = 0; // pin number to be sampled

void setup() {
  Serial.begin(9600);
  pinMode(analog_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if(Serial.available() > 0) {
    int command = Serial.parseInt();
    switch(command) {
      case 0: { // stop acquisition
        break;
      }
      case 1: { // start acquisition
        digitalWrite(LED_BUILTIN, HIGH);
        Serial.println(analogRead(analog_pin));
        digitalWrite(LED_BUILTIN, LOW);
        break;
      }
      default: { // acquire for the recieved duration */
        int led = t.oscillate(LED_BUILTIN, 500, HIGH);
        float duration = command * 1000; // ms
        float interval = 1/sampling_frequency*1000; // ms
        while (duration > 0) {
          Serial.print(String(analogRead(analog_pin)) + '\r');
          duration = duration - interval;
          delay(interval);
          t.update();
        }
        Serial.print('\n');
        t.stop(led);
        digitalWrite(LED_BUILTIN, LOW);
        break;
      }
    }
  }
}
