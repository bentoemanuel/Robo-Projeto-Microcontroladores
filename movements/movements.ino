#include <Servo.h>
#include <LedControl.h>

LedControl matrixA = LedControl(12,11,10,1);
LedControl matrixB = LedControl(7,9,8,1);
//Adafruit_8x8matrix matrixB = Adafruit_8x8matrix();
static const uint8_t PROGMEM a[][8] = { { B00000000,
                                          B00000000,
                                          B00011000,
                                          B00111100,
                                          B00111100,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00110000,
                                          B01000000,
                                          B00011000,
                                          B00011000,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00111100,
                                          B01001110,
                                          B01001110,
                                          B01111010,
                                          B01000010,
                                          B00111100,
                                          B00000000 },
                                        { B10101010,
                                          B10101010,
                                          B10111010,
                                          B01000100,
                                          B01000100,
                                          B01000100,
                                          B01000100,
                                          B00111000 },
                                        { B00000000,
                                          B00000000,
                                          B00111000,
                                          B01000100,
                                          B01000100,
                                          B01110100,
                                          B01110100,
                                          B00111000 },
                                        { B00000000,
                                          B01000000,
                                          B00100000,
                                          B00011000,
                                          B00000100,
                                          B00011000,
                                          B00100000,
                                          B00000000 },
                                        { B00000000,
                                          B00010000,
                                          B00111000,
                                          B01010000,
                                          B00111000,
                                          B00010100,
                                          B00111000,
                                          B00010000 },
                                        { B00000000,
                                          B00111000,
                                          B01000000,
                                          B00011000,
                                          B00011000,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00110000,
                                          B01000000,
                                          B00000000,
                                          B00111100,
                                          B01000010,
                                          B00000000,
                                          B00000000 },
                                        { B01111000,
                                          B10000000,
                                          B00111000,
                                          B01110100,
                                          B01110100,
                                          B01000100,
                                          B00111000,
                                          B00000000 },
                                        { B00011000,
                                          B00011000,
                                          B01111110,
                                          B11111111,
                                          B01111110,
                                          B00111100,
                                          B01100110,
                                          B01000010 },
                                        { B00000000,
                                          B00000000,
                                          B00000000,
                                          B00111000,
                                          B01001100,
                                          B00001100,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00000000,
                                          B00000000,
                                          B00111100,
                                          B01000100,
                                          B00000000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B10000000,
                                          B01111111,
                                          B01111100,
                                          B01111100,
                                          B00111000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B10000000,
                                          B01111111,
                                          B01001010,
                                          B01001010,
                                          B01000010,
                                          B00111100,
                                          B00000000 },
                                        { B00000000,
                                          B00000000,
                                          B00000000,
                                          B00000000,
                                          B01111000,
                                          B00000000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B01100000,
                                          B00000000,
                                          B00111000,
                                          B01001100,
                                          B00001100,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00111100,
                                          B01011010,
                                          B01011010,
                                          B01000010,
                                          B01000010,
                                          B00111100,
                                          B00000000 },
                                        { B00000000,
                                          B01110000,
                                          B10000000,
                                          B00111100,
                                          B01100110,
                                          B00100100,
                                          B00100100,
                                          B00100100 },
                                        { B00000000,
                                          B00111000,
                                          B01000100,
                                          B01011100,
                                          B01011100,
                                          B01000100,
                                          B00111000,
                                          B00000000 },
                                        { B00000000,
                                          B00000000,
                                          B00000000,
                                          B01000010,
                                          B00100100,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00110000,
                                          B01000000,
                                          B00011000,
                                          B00011000,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B01100000,
                                          B00010000,
                                          B00001100,
                                          B00010000,
                                          B00100000,
                                          B01000000,
                                          B00000000 },
                                        { B00000000,
                                          B00000000,
                                          B00101000,
                                          B01111100,
                                          B00111000,
                                          B00010000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B01000010,
                                          B00100100,
                                          B00011000,
                                          B00011000,
                                          B00100100,
                                          B01000010,
                                          B00000000 },
                                        { B00000000,
                                          B00111000,
                                          B01000100,
                                          B01110100,
                                          B01110100,
                                          B01000100,
                                          B00111000,
                                          B00000000 } };
static const uint8_t PROGMEM b[][8] = { { B00000000,
                                          B00000000,
                                          B00011000,
                                          B00111100,
                                          B00111100,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00000010,
                                          B00000100,
                                          B00011000,
                                          B00100000,
                                          B00011000,
                                          B00000100,
                                          B00000000 },
                                        { B00000000,
                                          B00111100,
                                          B01001110,
                                          B01001110,
                                          B01111010,
                                          B01000010,
                                          B00111100,
                                          B00000000 },
                                        { B01010101,
                                          B01010101,
                                          B01011101,
                                          B00100010,
                                          B00100010,
                                          B00100010,
                                          B00100010,
                                          B00011100 },
                                        { B00000000,
                                          B00000000,
                                          B00011100,
                                          B00101110,
                                          B00101110,
                                          B00100010,
                                          B00100010,
                                          B00011100 },
                                        { B00000000,
                                          B00000010,
                                          B00000100,
                                          B00011000,
                                          B00100000,
                                          B00011000,
                                          B00000100,
                                          B00000000 },
                                        { B00000000,
                                          B00001000,
                                          B00011100,
                                          B00101000,
                                          B00011100,
                                          B00001010,
                                          B00011100,
                                          B00001000 },
                                        { B00001100,
                                          B00010010,
                                          B00000001,
                                          B00011000,
                                          B00011000,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00001100,
                                          B00000010,
                                          B00000000,
                                          B00111100,
                                          B01000010,
                                          B00000000,
                                          B00000000 },
                                        { B00011100,
                                          B00100010,
                                          B01011101,
                                          B00111010,
                                          B00111010,
                                          B00100010,
                                          B00011100,
                                          B00000000 },
                                        { B00011000,
                                          B00011000,
                                          B01111110,
                                          B11111111,
                                          B01111110,
                                          B00111100,
                                          B01100110,
                                          B01000010 },
                                        { B00000000,
                                          B00000000,
                                          B00000000,
                                          B00011100,
                                          B00110010,
                                          B00110000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00000000,
                                          B00000000,
                                          B00111100,
                                          B00100010,
                                          B00000000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00000001,
                                          B11111110,
                                          B00111110,
                                          B00111110,
                                          B00011100,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00000001,
                                          B11111110,
                                          B01010010,
                                          B01010010,
                                          B01000010,
                                          B00111100,
                                          B00000000 },
                                        { B00000000,
                                          B00000000,
                                          B00000000,
                                          B00000000,
                                          B00011110,
                                          B00000000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00000110,
                                          B00000000,
                                          B00011100,
                                          B00100110,
                                          B00000110,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00111100,
                                          B01011010,
                                          B01011010,
                                          B01000010,
                                          B01000010,
                                          B00111100,
                                          B00000000 },
                                        { B00000000,
                                          B00001110,
                                          B00000001,
                                          B00111100,
                                          B01100110,
                                          B00100100,
                                          B00100100,
                                          B00100100 },
                                        { B00000000,
                                          B00011100,
                                          B00100010,
                                          B00111010,
                                          B00111010,
                                          B00100010,
                                          B00011100,
                                          B00000000 },
                                        { B00000000,
                                          B00000000,
                                          B00000000,
                                          B01000010,
                                          B00100100,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00001100,
                                          B00000010,
                                          B00011000,
                                          B00011000,
                                          B00011000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B00000110,
                                          B00001000,
                                          B00110000,
                                          B00001000,
                                          B00000100,
                                          B00000010,
                                          B00000000 },
                                        { B00000000,
                                          B00000000,
                                          B00010100,
                                          B00111110,
                                          B00011100,
                                          B00001000,
                                          B00000000,
                                          B00000000 },
                                        { B00000000,
                                          B01000010,
                                          B00100100,
                                          B00011000,
                                          B00011000,
                                          B00100100,
                                          B01000010,
                                          B00000000 },
                                        { B00000000,
                                          B00011100,
                                          B00100010,
                                          B00111010,
                                          B00111010,
                                          B00100010,
                                          B00011100,
                                          B00000000 } };

Servo boca1;
Servo boca2;


int inc = 0;
boolean readMode;
boolean mic;
boolean load;
int load_x[] = { 2, 3, 4, 5, 6, 6, 6, 6, 5, 4, 3, 2, 1, 1, 1, 1 };
int load_y[] = { 1, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 6, 5, 4, 3, 2 };
float load_i = 0;

void abre(float intensidade) {
  if (intensidade > 1.0) intensidade = 1.0;
  if (intensidade < 0.0) intensidade = 0.0;

  boca1.write(180 - (180 * intensidade));
  boca2.write(180 * intensidade);
}

void setup() {
  Serial.begin(9600); 

  boca1.attach(5);
  boca2.attach(6);
  
  boca1.write(180);
  boca2.write(0);

  matrixA.shutdown(0,false);
  matrixA.setIntensity(0,8);
  matrixA.clearDisplay(0);

  matrixB.shutdown(0,false);
  matrixB.setIntensity(0,8);
  matrixB.clearDisplay(0);

  // for (int i = 1; i<27;i++) {
  //   matrixA_showface(i);    
  //   matrixB_showface(i);
  //   delay(300);
  // }
}
String ap = "";
void loop() {
  if (load) {
    matrixA.clearDisplay(0);
    matrixB.clearDisplay(0);
    int li = floor(load_i);
    matrixA.setLed(0, 7 - load_x[li], load_y[li], true);
    matrixB.setLed(0, 7 - load_x[li], load_y[li], true);
    load_i = load_i > 15 ? 0 : (load_i + 0.1);
  }

  if (Serial.available() > 0) {
    String inc = Serial.readStringUntil('\n');
    inc.trim();
    Serial.println(inc);
    
    if (inc == "A") {
      mic = true;
      matrixB.setLed(0, 0, 7, true);
    } 
    else if (inc == "B") {
      mic = false;
      load = true;
    } 
    else if (inc == "C") {
      readMode = true;
      ap = "";
    } 
    else if (inc == "D") {
      load = false;
      readMode = false;
      
      int f = ap.toInt(); 
      
      if (f > 0 && f <= 27) { 
        matrixA.clearDisplay(0);
        matrixA_showface(f);
        matrixB_showface(f);
      } else {
        Serial.println("Erro: Rosto invalido!");
      }
      
      ap = ""; 
    } 
    else if (readMode) {
      ap = ap + inc;
    } 
    else {
      float intensidade = inc.toFloat();
      abre(intensidade);
    }
  }
}

void matrixA_showface(int f) {


matrixA.clearDisplay(0);
matrixA.setColumn(0, 7, pgm_read_byte(&(a[f-1][0])));
  matrixA.setColumn(0, 6, pgm_read_byte(&(a[f-1][1])));
  matrixA.setColumn(0, 5, pgm_read_byte(&(a[f-1][2])));
  matrixA.setColumn(0, 4, pgm_read_byte(&(a[f-1][3])));
  matrixA.setColumn(0, 3, pgm_read_byte(&(a[f-1][4])));
  matrixA.setColumn(0, 2, pgm_read_byte(&(a[f-1][5])));
  matrixA.setColumn(0, 1, pgm_read_byte(&(a[f-1][6])));
  matrixA.setColumn(0, 0, pgm_read_byte(&(a[f-1][7])));


}

void matrixB_showface(int f) {

matrixB.clearDisplay(0);
matrixB.setColumn(0, 7, pgm_read_byte(&(b[f-1][0])));
  matrixB.setColumn(0, 6, pgm_read_byte(&(b[f-1][1])));
  matrixB.setColumn(0, 5, pgm_read_byte(&(b[f-1][2])));
  matrixB.setColumn(0, 4, pgm_read_byte(&(b[f-1][3])));
  matrixB.setColumn(0, 3, pgm_read_byte(&(b[f-1][4])));
  matrixB.setColumn(0, 2, pgm_read_byte(&(b[f-1][5])));
  matrixB.setColumn(0, 1, pgm_read_byte(&(b[f-1][6])));
  matrixB.setColumn(0, 0, pgm_read_byte(&(b[f-1][7])));


}