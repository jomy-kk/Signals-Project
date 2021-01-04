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
  pinMode(analog_pin_a, INPUT);
  pinMode(analog_pin_b, INPUT);
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
  String samples = String(analog_pin_a) + ':' + String(analogRead(analog_pin_a)) + ';' + String(analog_pin_b) + ':' + String(analogRead(analog_pin_b));
  Serial.println(samples);
  /*Serial.print(analog_pin_a);
  Serial.print(":");
  Serial.print(analogRead(analog_pin_a));
  Serial.print(";");
  Serial.print(analog_pin_b);
  Serial.print(":");
  Serial.println(analogRead(analog_pin_b));*/
}
