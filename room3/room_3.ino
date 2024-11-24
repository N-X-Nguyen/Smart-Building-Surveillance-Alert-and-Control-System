// khai báo thư viện:
#include <ESP8266WiFi.h>
#include <MQUnifiedsensor.h>
#include <PubSubClient.h>
#include "DHT.h"
#define DHTTYPE DHT11   
#include<Arduino_JSON.h>
// ----------------------------------------------------------------------------------------------------------------------------------
// khai báo biến:
long now = millis();
long lastMeasure = 0;
JSONVar data;
bool phong3 = 1;
float t;
float h;
float Nh3;
float lux;
float last_temp = 0;
float last_humi = 0;
float last_Nh3 = 0;
float last_CO = 0;
float last_CO2 = 0;
float last_Alcohol = 0;
// ----------------------------------------------------------------------------------------------------------------------------------
//thông tin wifi và MQTT:
const char* ssid = "smarthome2011";
const char* password = "20112001H";
const char* mqtt_server = "192.168.0.185";
WiFiClient espClient3;
PubSubClient clientP2(espClient3);
// ----------------------------------------------------------------------------------------------------------------------------------
// DHT Sensor
const int DHTPin = 14;
// ----------------------------------------------------------------------------------------------------------------------------------
// Initialize DHT sensor.
DHT dht(DHTPin, DHTTYPE);
// ----------------------------------------------------------------------------------------------------------------------------------
// Timers auxiliar variables
MQUnifiedsensor MQ135("ESP8266",5, 10, A0, "MQ-135");
// ----------------------------------------------------------------------------------------------------------------------------------
//setup wifi:
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}
// ----------------------------------------------------------------------------------------------------------------------------------
void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
}
// ----------------------------------------------------------------------------------------------------------------------------------
//kết nối lại:
void reconnect() {
  // Loop until we're reconnected
  while (!clientP2.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (clientP2.connect("ESP8266Client3")) {
      Serial.println("connected");  
    } else {
      Serial.print("failed, rc=");
      Serial.print(clientP2.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
// ----------------------------------------------------------------------------------------------------------------------------------
// setup cảm biến:
void setup() {
  Serial.begin(115200);
  dht.begin();
  MQ135.setRegressionMethod(1); //_PPM =  a*ratio^b
  MQ135.init(); 
  MQ135.setRL(1);
  float calcR0 = 0;
  for(int i = 1; i<=10; i ++)
  {
    MQ135.update(); // Update data, the arduino will be read the voltage on the analog pin
    calcR0 += MQ135.calibrate(3.6);
  }
  MQ135.setR0(calcR0/10);
  if(isinf(calcR0)) {while(1);}
  if(calcR0 == 0){while(1);}
  setup_wifi();
  clientP2.setServer(mqtt_server, 1883);
  clientP2.setCallback(callback);
}
// ----------------------------------------------------------------------------------------------------------------------------------
//vòng lặp:
void loop() 
{
    if (!clientP2.connected()) {
    reconnect();
  }
  if(!clientP2.loop())
  clientP2.connect("ESP8266Client3");
  MQ135.update();
  h = dht.readHumidity();
  h = round(h * 10)/10;
  t = dht.readTemperature();
  t = round(t * 10)/10; 
  MQ135.setA(102.2); MQ135.setB(-2.473); 
  float NH3 = MQ135.readSensor();
  NH3 = round(NH3 * 10)/10;
  MQ135.setA(605.18); MQ135.setB(-3.937); 
  float CO = MQ135.readSensor(); 
  CO = round(CO * 10)/10;
  MQ135.setA(77.255); MQ135.setB(-3.18); 
  float Alcohol = MQ135.readSensor(); 
  Alcohol = round(Alcohol * 10)/10;
  MQ135.setA(110.47); MQ135.setB(-2.862); 
  float CO2 = MQ135.readSensor(); 
  CO2 = round((CO2 * 10) / 10)+400;
// ----------------------------------------------------------------------------------------------------------------------------------
// sử lí chuỗi Json.
    data["phong3"] = phong3;
    data["temp3"] = t;
    data["humi3"] = h;
    data["Nh33"] = NH3;
    data["3CO"] = CO;
    data["CO23"] = CO2;
    data["Alcoho3"] = Alcohol;
    String jsonString = JSON.stringify(data);
// ----------------------------------------------------------------------------------------------------------------------------------
// so sánh với giá trị cũ khi có giá trị mới rồi mới gửi.
  now = millis();
  if (now - lastMeasure > 10000) {
    lastMeasure = now;
    if(t != last_temp || h !=last_humi || NH3 != last_Nh3 || CO != last_CO || CO2 != last_CO2 || Alcohol !=last_Alcohol){
      t = last_temp ;
      h = last_humi;
      NH3 = last_Nh3;
      CO = last_CO;
      CO2 = last_CO2;
      Alcohol = last_Alcohol;
      clientP2.publish("/PHONG3", jsonString.c_str());  
    }
  }
  delay(500);
}