#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int temp = 0;
int tempe = 0;
void setup() {
  Serial.begin(9600);
  pinMode(temp, INPUT);
  lcd.begin(16, 2);
}

void loop() {
  lcd.clear();
  int reading = analogRead(temp);  
  float voltage = reading * 5.0;
  voltage /= 1024.0; 
  float temperatureC = (voltage - 0.5) * 100 ;  //converting from 10 mv per degree wit 500 mV offset
                                               //to degrees ((voltage - 500mV) times 100)
  lcd.print(temperatureC); lcd.println(" graus C");
  if (tempe == 0) {
    Serial.println(temperatureC);
    tempe = 1;
  }
  String leitura = Serial.readString();
  if (leitura.length() > 2) {
    lcd.clear();
    lcd.print(leitura);
    for (int scrollCounter = 0; scrollCounter < 40; scrollCounter++) 
    { 
      lcd.scrollDisplayLeft(); 
      delay(250);
    }
    lcd.clear();
    Serial.println("");
  }
}
