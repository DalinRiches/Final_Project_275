
#include <Arduino.h>


void setup(){
  //set digital pins 0-7 as outputs
  for (int i=3;i< 11;i++){
    pinMode(i,OUTPUT);
  }

  Serial.begin(115200);
}

uint8_t DAC(uint8_t input){

  uint8_t value = input;

  if ((value << 7)>>7 != 0){
    digitalWrite(3,HIGH);
  }
  else {
    digitalWrite(3,LOW);
  }

  value = input;

  if ((value << 6)>>7 != 0){
    digitalWrite(4, HIGH);
  }
  else {
    digitalWrite(4, LOW);
  }

  value = input;

  if ((value << 5)>>7 != 0){
    digitalWrite(5, HIGH);
  }
  else {
    digitalWrite(5, LOW);
  }

  value = input;

  if ((value << 4)>>7 != 0){
    digitalWrite(6,HIGH);
  }
  else {
    digitalWrite(6,LOW);
  }

  value = input;

  if ((value << 3)>>7 != 0){
    digitalWrite(7, HIGH);
  }
  else {
    digitalWrite(7, LOW);
  }

  value = input;

  if ((value << 2)>>7 != 0){
    digitalWrite(8, HIGH);
  }
  else {
    digitalWrite(8, LOW);
  }

  value = input;

  if ((value << 1)>>7 != 0){
    digitalWrite(9,HIGH);
  }
  else {
    digitalWrite(9,LOW);
  }

  value = input;

  if ((value)>>7 != 0){
    digitalWrite(10,HIGH);
  }
  else {
    digitalWrite(10,LOW);
  }


  return value;

}

int main(){
   setup();

   uint8_t bytes[10] = {0};
   int len_bytes = 0;





   while (true){

     len_bytes = Serial.readBytesUntil('\n', bytes, 10);

     Serial.println(bytes[0]);
     DAC(bytes[0]);

   }


  Serial.end();
}
