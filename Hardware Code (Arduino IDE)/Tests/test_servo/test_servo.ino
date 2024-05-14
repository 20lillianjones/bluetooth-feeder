#include <Servo.h>

Servo myServo;

void setup() {
  // put your setup code here, to run once:
  myServo.attach(3);
  myServo.write(180);
}

void loop() {
  // put your main code here, to run repeatedly:

}
