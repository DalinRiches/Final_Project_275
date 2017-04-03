#include <Arduino.h>


void setup() {
    // Arduino setup
    init();
    Serial.begin(2000000);

    // set digital pins 3-10 as outputs
    for (int i = 3; i < 11; ++i) {
        pinMode(i, OUTPUT);
    }

    Serial.println("Connection secured");
}

uint8_t DAC(uint8_t input) {
    // Loop through the bits
    for (int i = 0; i < 8; ++i) {
        if ((1 << i) & input) {
            digitalWrite(10 - i, HIGH);
        }
        else {
            digitalWrite(10 - i, LOW);
        }
    }
}

int main() {
    setup();


    // holds the current byte
    char byte;

    DAC(6);

    while(true){

        if (Serial.available() > 0) {
            // read the incoming byte
            byte = Serial.read();
            // Echo
            DAC((uint8_t)byte);

        }
    }

    Serial.end();
    return 0;
}
