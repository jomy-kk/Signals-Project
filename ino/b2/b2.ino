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

// variable that controls acquisition; either 0 or 1
volatile int acquire = 0;

void setup() {
  Serial.begin(19200);

  // Pin modes
  pinMode(analog_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

// acquisition by pooling
void loop() {
  t.update();

  // Update acquire status
  if(Serial.available() > 0) { // is there an instruction from the computer?
    int command = Serial.parseInt(); // get instruction from computer
    switch(command) {
      case 0: { // stop acquisition
        if (led_blinking == true) {
          t.stop(led_id); // stop blinking LED
          led_blinking = false;
        }
        acquire = 0; // stop
        break;
      }
      case 1: { // start acquisition
        if (led_blinking == false) {
            led_id = t.oscillate(LED_BUILTIN, 500, HIGH); // start blinking LED
            led_blinking = true;
          }
        acquire = 1; // start
        break;
      }
    }
  }

  // Acquire a sample?
  if(acquire) {
    Serial.println(String(millis()) + ':' + String(analogRead(analog_pin)));
    // Serial.read(); // uncomment to test ad-hoc
  }

  delay(1/sampling_frequency*1000); // wait until the next pool
}
