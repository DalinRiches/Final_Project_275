#include <Arduino.h>



void setup() {
    // Arduino setup
    init();
    Serial.begin(9600);

    // set digital pins 3-10 as outputs
    for (int i = 3; i < 11; ++i) {
        pinMode(i, OUTPUT);
    }

    //Serial.println("Connection secured");
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
    char sound[8100];


    DAC(6);

    while(Serial.available() == 0){

    }

    if (Serial.available() > 0){
      for (int i = 0; i < 8100; i++){
        while(true){
          byte = Serial.read();
          if (byte == 'T'){
            break;
          }
        sound[i] = Serial.read();
        delayMicroseconds(45);
        Serial.write('R');
        DAC(sound[i]);
        }
      }
    }


    Serial.end();

    while(true){

      for (int i = 0; i < 8100; i++){
        DAC(sound[i]);
        delayMicroseconds(45);
      }
      delay(1);
    }








    return 0;
}
