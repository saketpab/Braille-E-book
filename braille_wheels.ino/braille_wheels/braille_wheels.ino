#include <Stepper.h>

//Motor configuration 
const int STEPS_PER_FACE  = 500;   
const int TOTAL_FACES     = 8;

//Initialize stepper motors
// Stepper(steps_per_revolution, pin1, pin2)
Stepper leftWheel(STEPS_PER_FACE * TOTAL_FACES, 2, 3);
Stepper rightWheel(STEPS_PER_FACE * TOTAL_FACES, 4, 5);

//Initialize wheels
int leftCurrentFace  = 0;
int rightCurrentFace = 0;


void setup() {
  leftWheel.setSpeed(20);   
  rightWheel.setSpeed(20);

  Serial.begin(9600);
  Serial.println("READY");
}

//Shortest-path spin to a target face
void spinToFace(Stepper &wheel, int &currentFace, int targetFace) {
  if (currentFace == targetFace) return;

  int forward  = (targetFace - currentFace + TOTAL_FACES) % TOTAL_FACES;
  int backward = TOTAL_FACES - forward;

  if (forward <= backward) {
    wheel.step(forward * STEPS_PER_FACE);    
    Serial.print("Spinning forward ");
    Serial.print(forward);
    Serial.print(" face(s) to face ");
    Serial.println(targetFace);
  } else {
    wheel.step(-backward * STEPS_PER_FACE);  
    Serial.print("Spinning backward ");
    Serial.print(backward);
    Serial.print(" face(s) to face ");
    Serial.println(targetFace);
  }

  currentFace = targetFace;
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    int commaIndex = input.indexOf(',');
    if (commaIndex == -1) {
      Serial.println("ERROR: bad format, expected left,right");
      return;
    }

    int leftTarget  = input.substring(0, commaIndex).toInt();
    int rightTarget = input.substring(commaIndex + 1).toInt();

    if (leftTarget  < 0 || leftTarget  >= TOTAL_FACES ||
        rightTarget < 0 || rightTarget >= TOTAL_FACES) {
      Serial.println("ERROR: face number out of range (0-7)");
      return;
    }

    spinToFace(leftWheel,  leftCurrentFace,  leftTarget);
    spinToFace(rightWheel, rightCurrentFace, rightTarget);

    Serial.println("OK");
  }
}