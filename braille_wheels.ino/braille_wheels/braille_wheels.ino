#include <Stepper.h>

// Motor configuration 
const int STEPS_PER_FACE  = 256;
const int TOTAL_FACES     = 8;

// Initialize stepper motors
Stepper leftWheel(STEPS_PER_FACE * TOTAL_FACES,  8, 10, 9, 11);
Stepper rightWheel(STEPS_PER_FACE * TOTAL_FACES, 4, 6, 5, 7);

// Track current faces
int leftCurrentFace  = 0;
int rightCurrentFace = 0;

void setup() {
  leftWheel.setSpeed(10);   
  rightWheel.setSpeed(10);

  Serial.begin(9600);
  Serial.println("READY");
}

// Spin to target face
void spinToFace(Stepper &wheel, int &currentFace, int targetFace, bool isRight) {
  Serial.print("Current: ");
  Serial.print(currentFace);
  Serial.print(" Target: ");
  Serial.println(targetFace);

  if (currentFace == targetFace) return;

  int forward  = (targetFace - currentFace + TOTAL_FACES) % TOTAL_FACES;
  int backward = TOTAL_FACES - forward;

  if (forward <= backward) {
    Serial.print("Spinning forward ");
    if (isRight)
      {forward = -forward;}
    Serial.println(forward);
    wheel.step(forward * STEPS_PER_FACE);
  } else {
    Serial.print("Spinning backward ");
    if (isRight)
      {backward = -backward;}
    Serial.println(backward);
    wheel.step(-backward * STEPS_PER_FACE);
  }

  currentFace = targetFace;
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readString();   // Main Change, maybe /n was breaking stuff.

    input.trim();

    Serial.print("Received: [");
    Serial.print(input);
    Serial.println("]");

    int commaIndex = input.indexOf(',');
    if (commaIndex == -1) {
      Serial.println("ERROR: bad format");
      return;
    }

    int leftTarget  = input.substring(0, commaIndex).toInt();
    int rightTarget = input.substring(commaIndex + 1).toInt();

    if (leftTarget < 0 || leftTarget >= TOTAL_FACES ||
        rightTarget < 0 || rightTarget >= TOTAL_FACES) {
      Serial.println("ERROR: out of range");
      return;
    }

    spinToFace(leftWheel,  leftCurrentFace,  leftTarget, false);
    spinToFace(rightWheel, rightCurrentFace, rightTarget, true);

    Serial.println("OK");
  }
}
