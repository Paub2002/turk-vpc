// INVERSE KINEMATIKS explication in root path (as a png)

#include <Math.h>

#define PI 3.1415926535897932384626433832795

double upperLimb = 20;
double forearm = 20;

double lleyDelCos(double A, double B, double C) {
  double div = (A*A + B*B - C*C) / (2*A*B);
  if (div < -1.0) div = -1.0;
  if(div > 1.0) div = 1.0;
  return acos(div);
}

double distance(double x, double y) {
  return sqrt(x*x + y*y);
}

double radiansToDegrees(double radianes) {
  return radianes * 180.0 / PI;
}

void inverseKinematics(double x, double y, double& a1, double& a2) {
  double dist = distance(x, y);  
  double D1 = atan2(y, x);
  
  double D2 = lleyDelCos(dist, upperLimb, forearm);
  
  double a1Radianes = D1 + D2;
  double a2Radianes = abs(PI/2 - lleyDelCos(upperLimb, forearm, dist));
 
  a1 = radiansToDegrees(a1Radianes);
  a2 = radiansToDegrees(a2Radianes);

  Serial.print("IK-------- dist: "); Serial.println(dist);
  Serial.print("IK-------- D1 (degrees): "); Serial.println(radiansToDegrees(D1));
  Serial.print("IK-------- D1: "); Serial.println(D1);
  Serial.print("IK-------- D2(degrees): "); Serial.println(radiansToDegrees(D2));
  Serial.print("IK-------- D2: "); Serial.println(D2);
  Serial.print("-------- a1: "); Serial.println(a1);

}

double degreesToRadians(double degrees) {
    return degrees * PI / 180.0;
}

void kinematics(double a1, double a2, double& x, double& y) {
    // Convert angles from degrees to radians
    double a1Radianes = degreesToRadians(a1);
    double a2Radianes = degreesToRadians(a2);

    // Calculate the position (x, y) using direct kinematics
    x = upperLimb * cos(a1Radianes) + forearm * cos(a1Radianes + a2Radianes);
    y = upperLimb * sin(a1Radianes) + forearm * sin(a1Radianes + a2Radianes);
}
