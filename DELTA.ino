#include <TimerOne.h>

// Globals for Motor 1 and its encoder
const int M1encA = 2;
const int M1encB = 3;
const int M1CW = 4;//IN1 pin
const int M1CCW = 5;//IN2 pin
const int M1CPR = 64;

volatile bool M1Anow;
volatile bool M1Bnow;
volatile bool M1Apast;
volatile bool M1Bpast;
volatile int M1encCount = 0;
//End of Motor 1 and its encoder variables **********************************

//const int TimerOneInterval = 1000000;// 1 sec in microseconds

//Globals for PID ***********************************************************
int kp = 1, ki = 1, kd = 0;
float setRPM = 750, calcRPM = 0;
int M1PWM = 0;
const int M1PWR = 9;
int Err = 0, pastErr = 0, ErrSum = 0, dErr = 0;

//Interrupt Service Routines *************************************************

// M1ENC() used to write present and past values Motor1's encoder channels
void M1ENC(){
  M1Anow = digitalRead(M1encA);
  M1Bnow = digitalRead(M1encB);

  M1encCount += ParseEncoder();

  M1Apast = M1Anow;
  M1Bpast = M1Bnow;
  }
 // End of writing Encoder Channel A & B flip-flops ***************************
 int ParseEncoder(){
    if(M1Apast && M1Bpast){
    if(M1Anow && !M1Bnow) return 1;
    if(!M1Anow && M1Bnow) return -1;
  }else if(!M1Apast && M1Bpast){
    if(M1Anow && M1Bnow) return 1;
    if(!M1Anow && !M1Bnow) return -1;
  }else if(!M1Apast && !M1Bpast){
    if(!M1Anow && M1Bnow) return 1;
    if(M1Anow && !M1Bnow) return -1;
  }else if(M1Apast && !M1Bpast){
    if(!M1Anow && !M1Bnow) return 1;
    if(M1Anow && M1Bnow) return -1;
  }
 }
// End of ParseEncoder ******************************************************

void ISR_timerone(){
  Timer1.detachInterrupt();  // Stop the timer

  Serial.print("Set RPM: ");
  Serial.print(setRPM);
  Serial.print(" RPM -");

  Serial.print("  Motor1 PWM: ");
  Serial.print(M1PWM);

  Serial.print("- Encoder Ticks: ");
  Serial.print(M1encCount);

  Serial.print("  Motor1 Speed : ");
  calcRPM = (M1encCount / M1CPR) * 60.00;  // calculate RPM for Motor 1 = [(num. of counts in 1 sec)/(counts in 1 revolution)]x(60 seconds in 1 min.)
  //Counts per Rotation = 4 x PPR
  Serial.print(calcRPM);
  Serial.print(" RPM - ");
  M1encCount = 0;  //  reset counter to zero

  Serial.print("  Error : ");
  if(calcRPM < setRPM){
    Err = 1;
  }
  else if (calcRPM > setRPM){
    Err = -1;
  }
  else {
    Err = 0;
  }
  Serial.print(Err);

  Serial.print(" Error Sum: ");
  ErrSum += (ki*pastErr);
  pastErr = Err;
  Serial.print(ErrSum);
  Serial.print("\n");

  if(setRPM > 0){
    digitalWrite(M1CW, HIGH);
    digitalWrite(M1CCW, LOW);
  }
  else if(setRPM <0){
    digitalWrite(M1CW, LOW);
    digitalWrite(M1CCW, HIGH);
  }
  else if(setRPM == 0){
    digitalWrite(M1CW, LOW);
    digitalWrite(M1CCW, LOW);
  }
  M1PWM = (kp * Err) + ErrSum;

  Timer1.setPwmDuty(M1PWR, M1PWM);

  Timer1.attachInterrupt( ISR_timerone );  // Enable the timer
  }// End of ISR_timerone()

void setup() {
  Serial.begin(9600);

  pinMode(M1encA, INPUT);
  pinMode(M1encB, INPUT);
  pinMode(M1CW, OUTPUT);
  pinMode(M1CCW, OUTPUT);

  Timer1.initialize(500000); // set timer for 1sec
  Timer1.pwm(M1PWR, 0);
  attachInterrupt(digitalPinToInterrupt (M1encA), M1ENC, CHANGE);  // Increase counter 1 when speed sensor pin goes changes H/L->L/H
  attachInterrupt(digitalPinToInterrupt (M1encB), M1ENC, CHANGE);  // Increase counter 2 when speed sensor pin goes changes H/L->L/H
  Timer1.attachInterrupt( ISR_timerone ); // Enable the timer

}

void loop() {
  // put your main code here, to run repeatedly:

}
