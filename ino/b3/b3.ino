/*
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
*/

#include "Timer.h"
Timer t;

const float sampling_frequency = 320; // Hz
const int analog_pin_a = 0; // first pin number to be sampled
const int analog_pin_b = 5; // second pin number to be sampled

void setup() {
  Serial.begin(9600);

  // Pin modes
  pinMode(analog_pin_a, INPUT);
  pinMode(analog_pin_b, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  // LED interrupt
  digitalWrite(LED_BUILTIN, LOW);
  t.oscillate(LED_BUILTIN, 500, HIGH);

  // Sampling interrupt
  long interval = 1/sampling_frequency*1000; // ms
  t.every(interval, acquire, (void*)0);
}

void loop() {
  t.update();
}

void acquire() {
  // Send message with reads
  String samples = String(analog_pin_a) + ':' + String(analogRead(analog_pin_a)) + ';' + String(analog_pin_b) + ':' + String(analogRead(analog_pin_b));
  Serial.println(samples);
}
