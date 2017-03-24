
#include <Arduino.h>

void setup(){
  //set digital pins 0-7 as outputs
  for (int i=3;i<10;i++){
    pinMode(i,OUTPUT);
  }
}

int DAC(int value, int step_time){

  if ((value && 0b00000001)){
    digitalWrite(3,HIGH);
  }
  else {
    digitalWrite(3,LOW);
  }
  if ((value && 0b00000010)){
    digitalWrite(4, HIGH);
  }
  else {
    digitalWrite(4, LOW);
  }

  if ((value && 0b00000100)){
    digitalWrite(5, HIGH);
  }

  else {
    digitalWrite(5, LOW);
  }
  if ((value && 0b00001000)){
    digitalWrite(6,HIGH);
  }
  else {
    digitalWrite(6,LOW);
  }
  if ((value && 0b00010000)){
    digitalWrite(7, HIGH);
  }
  else {
    digitalWrite(7, LOW);
  }

  if ((value && 0b00100000)){
    digitalWrite(8, HIGH);
  }

  else {
    digitalWrite(8, LOW);
  }
  if ((value && 0b01000000)){
    digitalWrite(9,HIGH);
  }
  else {
    digitalWrite(9,LOW);
  }
  if ((value && 0b10000000)){
    digitalWrite(10,HIGH);
  }
  else {
    digitalWrite(10,LOW);
  }


  delayMicroseconds(step_time);
  return value;
}

int main(){
   setup();
  int step_time = 1;
  while (step_time < 1000) {
    /* code */
    

    int value = DAC(0, step_time);
    step_time = step_time + 1;

  }
}
