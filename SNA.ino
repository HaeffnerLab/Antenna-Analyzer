/* Author: Weerapat Pittayakanchit
 * Date: August 15, 2014
 * Brief: A Scalar Network Analyzer from AD9851 and Arduino Micro
 * Credit: 
 *         Andrew Smallbone <andrew@rocketnumbernine.com> for his code to command AD9851 to send a specific frequency
 *              www.rocketnumbernine.com/2011/10/25/programming-the-ad9851-dds-synthesizer
 *         Beric Dunn (K6BEZ) for his code to sweep through different frequencies and his circuit design for Attenna Analyzer
 *              www.hamstack.com/project_antenna_analyzer.html
 * Background:
 *         In the original design by Beric, he uses AD9850 which can only send a frequency upto 120MHz. I would like to be
 *         able to send a frequency upto 180MHz, so AD9851 which can send a frequency upto 180MHz better suits my purpose.
 * Usage:
 *         1. Connect the device that needed to be tested
 *         2. Connect the arduino to the PC
 *         3. Open the Serial Monitor (Assume you already setup the arduino IDE and can run basic applications smoothly)
 *         4. To start the sweeping, type in the starting frequency, the stop frequency,
 *            and the number of steps in the following format: xxxA xxxB xxxN S, where xxx are the numbers you want to set
 *            for the starting frequency, the stopping frequency, and the number of steps in between. S is the code to start
 *            sweeping.
 *            
 *            Ex: "2A 15B 1000N S" will perform the sweeping from 2 MHz to 15 MHz with 1000 steps.
 *
 *         5. The serial monitor will output the data in the following format
 *            current frequency in MHz, 100*(REV/FWD)^2, FWD, REV
 *            For more information, look at the Perform_sweep function at the end of the file.
 */

#define DATA 11   // connected to AD9851 D7 (serial data) pin 
#define W_CLK 9  // connected to AD9851 clock pin
#define FQ_UD 10  // connected to AD9851 device select pin
#define RESET 12  // connected to AD9851 device reset pin
#define pulseHigh(pin) {digitalWrite(pin, HIGH); digitalWrite(pin, LOW); }

double FWD=0;
double REV=0;
double Fstart = 1000000;  // Start Frequency for sweep
double Fstop = 10000000;  // Stop Frequency for sweep
double current_freq; // Temp variable used during sweep
long serial_input_number; // Used to build number from serial stream
int num_steps = 100; // Number of steps to use in the sweep
char incoming_char; // Character read from serial stream

// Andrew's code to send a specific signal
// transfer a byte a bit at a time LSB first to DATA
void tfr_byte(byte data)
{
  for (int i=0; i<8; i++, data>>=1) {
    digitalWrite(DATA, data & 00000001);
    pulseHigh(W_CLK);
  }
}

// frequency of signwave (datasheet page 12) will be <sys clock> * <frequency tuning word> / 2^32
void sendFrequency(double frequency) {
  int32_t freq = frequency * 4294967296.0 / 180.0e6;
  for (int b=0; b<4; b++, freq>>=8) {
    tfr_byte(freq & 0xFF);
  }
  tfr_byte(0x001);
  pulseHigh(FQ_UD);
}

void setup() {
  
 // all pins to outputs
  pinMode(FQ_UD, OUTPUT);
  pinMode(W_CLK, OUTPUT);
  pinMode(DATA, OUTPUT);
  pinMode(RESET, OUTPUT);

  // if your board needs it, connect RESET pin and pulse it to reset AD9851
  pulseHigh(RESET);

  // set serial load enable (Datasheet page 15 Fig. 17) 
  pulseHigh(W_CLK);
  pulseHigh(FQ_UD);
  //Serial.begin(9600); // set the baud rate
}

// Beric's code to sweep through different frequencies
void loop() {
  //Check for character
  if(Serial.available()>0){
    incoming_char = Serial.read();
    switch(incoming_char){
    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
      serial_input_number=serial_input_number*10+(incoming_char-'0');
      break;
    case 'A':
      //Turn frequency into FStart
      Fstart = (double) serial_input_number*1000000;
      serial_input_number=0;
      //Serial.print("Set start freq:");
      //Serial.println(Fstart);
      break;
    case 'B':
      //Turn frequency into FStop
      Fstop = (double) serial_input_number*1000000;
      serial_input_number=0;
      //Serial.print("Set stop freq:");
      //Serial.println(Fstop);
      break;
    case 'N':
      // Set number of steps in the sweep
      num_steps = serial_input_number;
      serial_input_number=0;
      //Serial.print("Set number of steps in sweep:");
      //Serial.println(num_steps);
      break;
    case 'S':
      //Serial.println("recorded 'S'");
    case 's':   
      Perform_sweep();
      //Serial.println("recorded 's', initialized sweep");
      break;
    case '?':
    // Report current configuration to PC    
      Serial.print("Start Freq:");
      Serial.println(Fstart);
      Serial.print("Stop Freq:");
      Serial.println(Fstop);
      Serial.print("Num Steps:");
      Serial.println(num_steps);
      break;
    }
    Serial.flush();     
  }
  delay(100);
}

void Perform_sweep(){
  double Fstep = (Fstop-Fstart)/num_steps;
  double gamma;
  //Serial.println("Performing sweep");
  // Start loop 
  for(int i=0;i<=num_steps;i++){
    // Calculate current frequency
    current_freq = Fstart + i*Fstep;
    // Set DDS to current frequency
    sendFrequency(current_freq);
    // Wait a little for settling (used to be 0.5)
    delay(0.2);
    // Read the forawrd and reverse voltages
    REV = analogRead(A0);
    FWD = analogRead(A1);
    if(FWD==0 || FWD < REV){
      // To avoid a divide by zero
      gamma = 100;
    }else{
      // Calculate reflected power
      gamma = 100*(REV*REV)/((FWD)*(FWD));
    }
    
    // Send current line back to PC over serial bus
    Serial.print(((double) current_freq)/1000000);
    Serial.print(" ");
    Serial.print(gamma);
    Serial.print(" ");
    Serial.print(FWD);
    Serial.print(" ");
    Serial.print(REV);
    Serial.println(" "); // get rid of \r &\n problem
  }
  Serial.flush();
}
