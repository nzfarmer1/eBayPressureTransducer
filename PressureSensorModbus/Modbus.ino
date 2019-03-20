#include <ModbusRtu.h>
#include <exponential_moving_average.h>


/**
 *  Modbus object declaration
 *  u8id : node id = 0 for master, = 1..247 for slave
 *  u8serno : serial port (use 0 for Serial)
 *  u8txenpin : 0 for RS-232 and USB-FTDI 
 *               or any pin number > 1 for RS-485
 */

#define MAX_STORED 12
#define ASIZE 4
uint16_t au16data[ASIZE];

void io_poll();

static SoftwareSerial serial(11,10);
static Modbus slave(1,4,0); // this is slave @1 and RS-232 or USB-FTDI
static ExponentialMovingAverage ema = ExponentialMovingAverage(MAX_STORED);

#define max(a,b) (a >= b) ? (a) : (b)

#define PMAX  30
#define PSTART 95.0
static const uint16_t Pv = PMAX*4; // 4 volts
static const float vrange = 1024*0.2; //0.5-4.5v




void setup() {
  Serial.begin(9600);
  //slave.begin( 9600 ); // baud-rate at 9600
  slave.begin(&serial,9600L);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
}

void loop() {
    slave.poll(au16data,ASIZE);
    io_poll();
}

void io_poll() {
  
  au16data[2] = analogRead(A0); 
  au16data[3] = analogRead(A1); 

  au16data[1] = ema.Add(au16data[2]);
  au16data[0] = (uint16_t) max((((float)au16data[1]-PSTART)/vrange)*Pv,0);
}
