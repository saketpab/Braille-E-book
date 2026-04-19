#include <Stepper.h>

const int STEPS_PER_FACE = 256;
const int TOTAL_FACES = 8;

// Motors (adjust pins for your setup)
Stepper left1(STEPS_PER_FACE * TOTAL_FACES,  8,10,9,11);
Stepper right1(STEPS_PER_FACE * TOTAL_FACES, 4,6,5,7);

Stepper left2(STEPS_PER_FACE * TOTAL_FACES,  22,24,23,25);
Stepper right2(STEPS_PER_FACE * TOTAL_FACES, 26,28,27,29);

// Current state
int l1 = 0, r1 = 0, l2 = 0, r2 = 0;

// Buffer for incoming characters
const int MAX_BUFFER = 20;
int bufferL[MAX_BUFFER];
int bufferR[MAX_BUFFER];
int bufferCount = 0;

void setup() {
  Serial.begin(9600);

  left1.setSpeed(10);
  right1.setSpeed(10);
  left2.setSpeed(10);
  right2.setSpeed(10);

  Serial.println("READY");
}

void spinToFace(Stepper &wheel, int &current, int target, bool isRight) {
  if (current == target) return;

  int forward  = (target - current + TOTAL_FACES) % TOTAL_FACES;
  int backward = TOTAL_FACES - forward;

  if (forward <= backward) {
    if(isRight)
      {forward = -forward;}
    
    wheel.step(forward * STEPS_PER_FACE);
  } else {
    if(isRight)
      {backward = -backward;}
    
    wheel.step(-backward * STEPS_PER_FACE);
  }

  current = target;
}

// Show two characters on 4 motors
void displayPair(int L1, int R1, int L2, int R2) {
  spinToFace(left1,  l1, L1, false);
  spinToFace(right1, r1, R1, true);
  spinToFace(left2,  l2, L2, false);
  spinToFace(right2, r2, R2, true);

  Serial.println("DISPLAYED PAIR");
}

void loop() {

  // 🔹 1. Read incoming stream
  if (Serial.available()) {
    String input = Serial.readString();
    input.trim();

    int commaIndex = input.indexOf(',');
    if (commaIndex != -1) {
      int left  = input.substring(0, commaIndex).toInt();
      int right = input.substring(commaIndex + 1).toInt();

      // store in buffer
      if (bufferCount < MAX_BUFFER) {
        bufferL[bufferCount] = left;
        bufferR[bufferCount] = right;
        bufferCount++;
      }

      Serial.print("Buffered: ");
      Serial.println(bufferCount);
    }
  }

  // 🔹 2. If we have at least 2 characters → display them
  if (bufferCount >= 2) {

    displayPair(
      bufferL[0], bufferR[0],
      bufferL[1], bufferR[1]
    );

    delay(10000);  // display time

    // 🔹 3. Shift buffer (remove first 2)
    for (int i = 2; i < bufferCount; i++) {
      bufferL[i-2] = bufferL[i];
      bufferR[i-2] = bufferR[i];
    }

    bufferCount -= 2;

    Serial.println("OK");  // Python waits for this
  }
}
