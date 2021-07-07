int pirPin = 7;               
int pirState = LOW;             
int motionDetected = 0;                    

void setup() {
  pinMode(pirPin, INPUT);     
  Serial.begin(9600);
}


void updateMotion(){
  motionDetected = digitalRead(pirPin);
  Serial.println(motionDetected);
  // if (motionDetected == HIGH) {            
  //   if (pirState == LOW) {
  //     Serial.println("Motion detected!");
  //     pirState = HIGH;
  //   }
  // } else {
  //   if (pirState == HIGH){
  //     Serial.println("Motion ended!");
  //     pirState = LOW;
  //   }
  // }
}
void loop(){
  updateMotion();
}
