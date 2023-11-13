const int ledPin = 13;  // Ajusta el pin del LED según tu configuración

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();
    
    if (signal == '1') {
      digitalWrite(ledPin, HIGH);  // Enciende el LED
      delay(5000);  // Mantiene el LED encendido por 5 segundos (ajusta según tus necesidades)
      digitalWrite(ledPin, LOW);  // Apaga el LED
    }
  }
}