//The sole purpose of this program is to test Serial communication...
//...from the PC to the HC-05 Bluetooth module
#include <Wire.h>
#include <SoftwareSerial.h>

void setup(){
  pinMode(9, OUTPUT);
  //Initialize Serial communication for Bluetooth module:
  Serial.begin(9600);
}

void loop(){
  getSerialInput();
}

void getSerialInput(){
  //Use function to read Serial input from the HC-05 module:
  while(1){ //Enter an infinite loop:
    if(Serial.available() > 0){ //if there is serial information to be read...
      char readChar = Serial.read(); //Read the received character and store it - should only get one character at a time
      digitalWrite(9, HIGH); // Print received data to serial monitor
      delay(3000);
      digitalWrite(9, LOW);
    }
  }
}