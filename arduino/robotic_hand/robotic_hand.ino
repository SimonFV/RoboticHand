#include <Servo.h> 

// Servomotores
Servo finger1;
Servo finger2;
Servo finger3;
Servo finger4;
Servo finger5;


String data = ""; // Mensaje recibido 
int servo = 0;    // Numero de motor
int pos = 0;      // Angulo para la posicion del motor
char c;           // Char que captura cada byte entrante

void setup() {
  // Liga los servomotores a los pines respectivos
  finger1.attach(15);
  finger2.attach(16);
  finger3.attach(17);
  finger4.attach(18);
  finger5.attach(19);

  // Abre la conexion serial
  Serial.begin(9600);
}

void loop() {
  // Espera por mensajes y los procesa
  if(Serial.available()>5){
    while(Serial.available()>0){
      c = Serial.read();
      if(c == 'b'){
        break;
      }
      if(c == ','){
        servo = data.toInt();
        data = "";
      }
      else{
        data += c;
      }
    }
    if(data != ""){
      pos = data.toInt();
      data = "";
    }
  }
  
  // Mueve el motor respectivo
  if(servo != 0){
    switch(servo){
      case 1:
        finger1.write(pos);
        break;
       case 2:
        finger2.write(pos);
        break;
       case 3:
        finger3.write(pos);
        break;
       case 4:
        finger4.write(pos);
        break;
       case 5:
        finger5.write(pos);
        break;
       case 6:
        finger1.write(pos);
        finger2.write(pos);
        finger3.write(pos);
        finger4.write(pos);
        finger5.write(pos);
        break;
    }
    servo = 0;
    pos = 0;
  }
}
