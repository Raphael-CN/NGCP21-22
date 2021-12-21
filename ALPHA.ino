#include <TimerOne.h>
// Include the TimerOne Library from Paul Stoffregen

const int Motor1A = 2;
const int Motor1B = 3;

// Constants for Interrupt Pins
const int MOTOR1A = 2;  // Motor 1 Interrupt Pin - INT 0
const int MOTOR1B = 3;  // Motor 2 Interrupt Pin - INT 1
// Change values if not using Arduino Uno


volatile bool Motor1Apast;//Motor Encoder CH.A&B past and present boolean states
volatile bool Motor1Bpast;
volatile bool Motor1Anow;
volatile bool Motor1Bnow;
volatile int Motor1counts = 0;


// Float for number of pulses per rotation
float PPR = 16;  // Change to match value of encoder disk


// Interrupt Service Routines

// Interrupt service routines for the Motor1's quadrature encoder
void Motor1Interrupt(){
  Motor1Anow = digitalRead(Motor1A);
  Motor1Bnow = digitalRead(Motor1B);

  Motor1counts+=ParseEncoder();

  Motor1Apast = Motor1Anow;
  Motor1Bpast = Motor1Bnow;
}

int ParseEncoder(){
  if(Motor1Apast && Motor1Bpast){
    if(!Motor1Anow && Motor1Bnow) return 1;
    if(Motor1Anow && !Motor1Bnow) return -1;
  }else if(!Motor1Apast && Motor1Bpast){
    if(!Motor1Anow && !Motor1Bnow) return 1;
    if(Motor1Anow && Motor1Bnow) return -1;
  }else if(!Motor1Apast && !Motor1Bpast){
    if(Motor1Anow && !Motor1Bnow) return 1;
    if(!Motor1Anow && Motor1Bnow) return -1;
  }else if(Motor1Apast && !Motor1Bpast){
    if(Motor1Anow && Motor1Bnow) return 1;
    if(!Motor1Anow && !Motor1Bnow) return -1;
  }
}

// TimerOne ISR
void ISR_timerone()
{
  Timer1.detachInterrupt();  // Stop the timer

  Serial.print("Encoder Ticks: ");
  Serial.print(Motor1counts);
  Serial.print("  Motor1 Speed : ");
  float rotation1 = (Motor1counts / (PPR*4)) * 60.00;  // calculate RPM for Motor 1 = [(num. of counts in 1 sec)/(counts in 1 revolution)]x(60 seconds in 1 min.)
  //Counts per Rotation = 4 x PPR
  Serial.print(rotation1);
  Serial.print(" RPM - ");
  Motor1counts = 0;  //  reset counter to zero
  Serial.print("\n");

  Timer1.attachInterrupt( ISR_timerone );  // Enable the timer
}
//
//
//Setup
//
//
void setup()
{
  Serial.begin(9600);

  pinMode(Motor1A, INPUT);
  pinMode(Motor1B, INPUT);

  Timer1.initialize(1000000); // set timer for 1sec
  attachInterrupt(digitalPinToInterrupt (Motor1A), Motor1Interrupt, CHANGE);  // Increase counter 1 when speed sensor pin goes High
  attachInterrupt(digitalPinToInterrupt (Motor1B), Motor1Interrupt, CHANGE);  // Increase counter 2 when speed sensor pin goes High
  Timer1.attachInterrupt( ISR_timerone ); // Enable the timer
}

void loop()
{
  // Nothing in the loop!
  // You can place code here
}
