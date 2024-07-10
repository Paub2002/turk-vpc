// Parser
void parseMessage(String command, int* coordinates) {
  for (int i = 0; i < command.length(); i++) {
    char coordinateChar = command.charAt(i);
    int coordinate = coordinateChar - '0';
    coordinates[i] = coordinate;
  }
}


void commandParser(String command) {
  int coordinates[COMMAND_LENGHT];
  parseMessage(command, coordinates);
  for (int i = 0; i <= 4; i++){
    Serial.println(command[i]);
  }
  moveToHc(coordinates[0], coordinates[1]);
  moveToHc(coordinates[2], coordinates[3]);
}

// Serial Reader
String readSerial() {
  String command = "";

  while (command.length() < 4) {
    while (Serial.available() > 0) {
      char inChar = (char)Serial.read();
      if (isDigit(inChar)) {
        command += inChar;
      }
      if (command.length() == 4) {
        break;
      }
    }
  }

  while (Serial.available() > 0) {
    Serial.read();
  }

  return command;
}


void sound() {
  tone(BUZZER, 600, 200);
}

// leds
void setStatusLed(int status) {
  switch(status) {
    case 0: 
      digitalWrite(STATUS_LED, LOW);
      break;
    case 1:
      sound();
      digitalWrite(STATUS_LED, HIGH);
      break;
    case 2: 
      sound();
      digitalWrite(STATUS_LED, HIGH);
      delay(200);
      digitalWrite(STATUS_LED, LOW);
      delay(200);
      digitalWrite(STATUS_LED, HIGH);
      delay(200);
      digitalWrite(STATUS_LED, LOW);
      break;
  }
}