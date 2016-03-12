#include <Servo.h>

Servo servo;
const int potpin = 1;
const int servopin = 8;
int potVal =0;

void setup() {
  Serial.begin(9600);
  servo.attach(servopin);   
} 

void loop() {

    if(Serial.available()>0){
       potVal = Serial.parseInt();
    }
  servo.write(map(potVal, 0, 1023, 0, 180)); 
}

// windows command prompt ipconfig
//   173.250.146.145
