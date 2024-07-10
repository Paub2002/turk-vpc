#include <Adafruit_MotorShield.h>
#include <Servo.h>
Servo elbow, shoulder, finger;

#define FINGER 2
#define SHOULDER 9
#define ELBOW 10

void setup_servos() {
  Serial.println("Setting up servos...");
  finger.attach(FINGER);
  shoulder.attach(SHOULDER);
  elbow.attach(ELBOW);
  delay(1000); // time to prepare servos
  Serial.println("Servos ready.");
}

void setToZero(){
  updateShoulder(0);
  updateElbow(0);
}

void updateElbow(int deg) {
  if (deg >= 0 && deg <= 180) {
    setStatusLed(1);
    elbow.write(deg);
    delay(200);
    setStatusLed(0);
  }
}

void updateShoulder(int deg) {
  if (deg >= 0 && deg <= 180) {
    setStatusLed(1);
    shoulder.write(deg);
    delay(200);
    setStatusLed(0);
  }
}

void updateFinger(int a) {
  finger.write(a);
}

void fingerController(int action) {
  if (action == 0) {
      s.write(100);
    } else if (action == 1){
      s.write(76.6);
    } else if (action == 2){
      s.write(63.3);
    } else if (action == 3){
      s.write(30);
    }
}

// with inverse kinematiks
void moveToIk(double x, double y) {
  Serial.print("Move to ("); Serial.print(x); Serial.print(", "); Serial.print(y); Serial.println(")");
  double alfa = 0, beta = 0;
  inverseKinematics(x, y, alfa, beta);
  // print results
  Serial.print("alfa: "); Serial.println(alfa);
  Serial.print("beta: "); Serial.println(beta);

  updateShoulder(alfa);
  updateElbow(beta);
}

// Hardcoded 
void moveToHc(int row, int col) {
  int matrix[8][8][3] = {
    {{70, 90, 3}, {80, 90, 3}, {73, 90, 1}, {73, 90, 1}, {73, 90, 1}, {90, 90, 2}, {90, 90, 2}, {96, 88, 2}},
    {{70, 90, 2}, {70, 90, 2}, {73, 90, 1}, {73, 90, 1}, {73, 90, 1}, {90, 90, 2}, {90, 90, 2}, {96, 88, 2}},
    {{70, 90, 1}, {70, 90, 1}, {73, 90, 0}, {73, 90, 0}, {62, 120, 0}, {62, 120, 0}, {90, 88, 0}, {90, 88, 0}},
    {{80, 70, 0}, {80, 70, 0}, {80, 90, 0}, {144, 5, 2}, {62, 120, 0}, {62, 120, 0}, {45, 170, 2}, {45, 170, 2}},
    {{15, 167, 1}, {15, 167, 1}, {144, 5, 1}, {144, 5, 1}, {40, 160, 0}, {40, 160, 0}, {45, 170, 2}, {45, 170, 2}},
    {{16, 170, 0}, {16, 170, 0}, {144, 5, 0}, {144, 5, 0}, {40, 160, 0}, {40, 160, 0}, {160, 5, 0}, {160, 5, 0}},
    {{16, 170, 0}, {16, 170, 0}, {160, 0, 1}, {160, 0, 1}, {20, 180, 0}, {20, 180, 0}, {160, 5, 0}, {160, 5, 0}},
    {{134, 3, 0}, {134, 3, 0}, {160, 0, 1}, {160, 0, 1}, {20, 180, 0}, {20, 180, 0}, {35, 180, 0}, {35, 180, 0}}
  };
  /*
  Serial.print(row);Serial.print(", ");Serial.println(col);
  Serial.print(matrix[row][col][0]);Serial.print(", ");Serial.println(matrix[row][col][1]);
  */
  updateShoulder(180);
  updateElbow(0);
  delay(1500);
  fingerController(matrix[row][col][2]);
  updateShoulder(matrix[row][col][0]);
  updateElbow(matrix[row][col][1]);
  setStatusLed(2);
  sound();
  setStatusLed(1);
  
  delay(2000);
  setStatusLed(0);
  updateShoulder(180);
  updateElbow(0);
}