#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>
#include <Servo.h>

//Create LCD screen/Servo motor objects:
LiquidCrystal_I2C lcd(0x20, 20, 4); //Initialize the LCD screen
Servo servoMotor;

//Determine delay for each of the feeding increments:
int shortDelay = 5;
int medDelay = 10;
int longDelay = 15;

void setup(){
  //Initialize Serial communication for Bluetooth module:
  Serial.begin(9600);
  servoMotor.attach(9); //Control Servo motor at digital pin 9 (yellow wire)

  //Initialize LCD display:
  lcd.init();
  lcd.backlight();
  lcd.setCursor(7, 0);
  lcd.print("Hello!");
  delay(3000);
  lcd.clear();
  lcd.setCursor(5, 0);
  lcd.print("Waiting...");

  //Initialize Servo motor:
  //servoMotor.write(90);

  //Quick-feed pin reading:
  pinMode(8, INPUT_PULLUP);
}

void loop(){
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

//Add LCD screen messages to the below function:
void feedAction(char readChar){
  if(readChar == 'A'){ //Shortest feeding interval:
    lcd.clear();
    lcd.setCursor(4, 0);
    lcd.print("Just a Snack");
    lcd.setCursor(6, 1);
    lcd.print("Feeding");
    lcd.setCursor(3, 2);
    lcd.print("in Progress...");

    turnMotor(shortDelay);
  }
  else if(readChar == 'B'){ //Medium-length feeding interval:
    lcd.setCursor(5, 0);
    lcd.print("Lunch Time");
    lcd.setCursor(6, 1);
    lcd.print("Feeding");
    lcd.setCursor(3, 2);
    lcd.print("in Progress...");

    turnMotor(medDelay);
  }
  else{ //Longest feeding interval:
    lcd.clear();
    lcd.setCursor(5, 0);
    lcd.print("CHOW DOWN!");
    lcd.setCursor(6, 1);
    lcd.print("Feeding");
    lcd.setCursor(3, 2);
    lcd.print("in Progress...");

    turnMotor(longDelay);
  }

  delay(10);
  lcd.clear();
  lcd.setCursor(5, 0);
  lcd.print("Waiting...");
}

void quickFeed(){
  lcd.clear();
  lcd.setCursor(7, 0);
  lcd.print("Quick");
  lcd.setCursor(6, 1);
  lcd.print("Feeding");
  lcd.setCursor(3, 2);
  lcd.print("in Progress...");

  turnMotor(medDelay);

  delay(10);
  lcd.clear();
  lcd.setCursor(5, 0);
  lcd.print("Waiting...");
}

void turnMotor(int servoInt){
  for(int i=0; i<=servoInt; i++){
    servoMotor.write(10);
    delay(1000);
    servoMotor.write(170);
    delay(1000);
    }
}