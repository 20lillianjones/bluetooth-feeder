#include <Wire.h>
#include <SoftwareSerial.h>
#include <Servo.h>

//Create LCD screen/Servo motor objects:
Servo servoMotor;

//Determine delay for each of the feeding increments:
int shortDelay = 5000;
int medDelay = 7500;
int longDelay = 10000;

void setup(){
  //Initialize Serial communication for Bluetooth module:
  //Serial.begin(9600);

  //Initialize Servo motor:
  servoMotor.attach(3); //Control Servo motor at digital pin 9 (yellow wire)
  servoMotor.write(75);
  delay(5000);
  servoMotor.write(15);
  delay(5000);
  //servoMotor.detach();

  //Quick-feed pin reading:
  pinMode(8, INPUT_PULLUP);

  //servoMotor.write(170);
  delay(2000);
}


void loop(){
  //sweepMotor(1000);
  char readChar = ""; //Initialize an empty variable to store serial input
  readChar = getSerialInput(); //Get serial data input
  feedAction(readChar); //Feed based on the Serial data received
}

char getSerialInput(){
  //Use function to read Serial input from the HC-05 module:
  char readChar = "";
  while(1){ //Enter an infinite loop:
    if(Serial.available() > 0){ //if there is serial information to be read...
      readChar = Serial.read(); //Read the received character and store it - should only get one character at a time
      break;
    }
    if(digitalRead(8) == HIGH){
      quickFeed();
    }
  }
  return readChar;
}

//Take action depending on the serially-received character:
void feedAction(char readChar){
  if(readChar == 'A'){ //Shortest feeding interval:
    sweepMotor(shortDelay);
  }
  else if(readChar == 'B'){ //Medium-length feeding interval:
    sweepMotor(medDelay);
  }
  else{ //Longest feeding interval:
    sweepMotor(longDelay);
  }
  delay(1000);
  //servoMotor.attach(2);
}

//Function to move the Servo motor for a desired amount of time:
void sweepMotor(int delayTime){
  servoMotor.write(120);
  delay(5000);
  servoMotor.write(90);
  servoMotor.detach();
}

//Function to activate feeding on the feeder itself by pressing a button:
void quickFeed(){
  sweepMotor(medDelay);
}