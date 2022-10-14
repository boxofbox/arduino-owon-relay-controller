int x, p;
const int controlPin[8] = {2,3,4,5,6,7,8,9};


void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(1);
  x = 0;
  digitalWrite(LED_BUILTIN, LOW);
  for (int i=0; i<8; i++) {
    pinMode(controlPin[i], OUTPUT);
    digitalWrite(controlPin[i], HIGH);
  }
}

// the loop function runs over and over again forever
void loop() {

  // check for program change
  if (Serial.available() > 0) {
    p = Serial.readString().toInt();
    if (p == 0) {
      clearRelayFun();
      switchRelay(p);
      x = p;      
    } else {
      switchRelay(p);
      x = p;      
    }
    Serial.print("switched to " + String(x) + "\n");
  } 
  blinkNTimes(x);
  digitalWrite(LED_BUILTIN, LOW);
  delay(2000); 
}

void clearRelayFun() {
  for (int i = 0; i < 20; i++) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(50);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(50);
  }
}

void switchRelay(int n) {
  if (x!=0) {
    digitalWrite(controlPin[x-1], HIGH);
  }
  if (n!=0) {
    digitalWrite(controlPin[n-1], LOW);
  }
}

void blinkNTimes(int n) {
  if (n == 0) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
  }
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(100);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(100);
  }
  return;
}
