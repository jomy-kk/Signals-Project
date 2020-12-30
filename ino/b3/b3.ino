/*
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
*/

#include "Timer.h"
Timer t;

const float sampling_frequency = 400; // Hz
const int analog_pin = 0; // pin number to be sampled

void setup() {
  Serial.begin(9600);
  pinMode(analog_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  t.oscillate(LED_BUILTIN, 500, HIGH);

  long interval = 1/sampling_frequency*1000; // ms
  t.every(interval, acquire, (void*)0);
}

void loop() {
  t.update();
}

void acquire() {
  Serial.println(analogRead(analog_pin));
}
