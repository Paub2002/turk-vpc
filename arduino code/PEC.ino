#define STATUS_LED 8
#define BUZZER 11

#define COMMAND_LENGHT 4

const int maxValues = 4;
int values[maxValues];
int currentValueIndex = 0;

void setup() {
  Serial.begin(9600);
  delay(100);

  sound();
  pinMode(STATUS_LED, OUTPUT);
  setup_servos();

  delay(500);
  updateShoulder(180);
  updateElbow(0);
  setStatusLed(2);

}

void loop() {
  String command = readSerial();
  commandParser(command);
}