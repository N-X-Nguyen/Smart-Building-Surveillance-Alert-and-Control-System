// khai báo thư viện:
#include <ESP8266WiFi.h>
#include <MQUnifiedsensor.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <Wire.h>
#include <BH1750.h>
#define DHTTYPE DHT11   
#include<Arduino_JSON.h>
// ----------------------------------------------------------------------------------------------------------------------------------
// khai báo biến:
BH1750 lightMeter;
JSONVar data;
bool phong2 = 1;
float t;
float h;
float Nh3;
float lux;
float last_temp = 0;
float last_humi = 0;
float last_Nh3 = 0;
float last_lux = 0;
float last_CO = 0;
float last_CO2 = 0;
float last_Alcohol = 0;
// ----------------------------------------------------------------------------------------------------------------------------------
//thông tin wifi và MQTT:
const char* ssid = "smarthome2011";
const char* password = "20112001H";
const char* mqtt_server = "192.168.0.185";
WiFiClient espClient;
PubSubClient clientP2(espClient);
// ----------------------------------------------------------------------------------------------------------------------------------
long now = millis();
long lastMeasure = 0;

// DHT Sensor
const int DHTPin = 14;
//các relay
const int relay1D = 0;
const int relay2D = 3;
const int relay3D = 12;
const int relay4D = 13;
const int relay5wind = 15;
const char* topic1 = "/phong2/relay";
// ----------------------------------------------------------------------------------------------------------------------------------
// Initialize DHT sensor.
DHT dht(DHTPin, DHTTYPE);
// ----------------------------------------------------------------------------------------------------------------------------------
// Timers auxiliar variables
MQUnifiedsensor MQ135("ESP8266",5, 17, A0, "MQ-135");
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
  if(topic == "/PHONG2/relay/")
{
  JSONVar data1 = JSON.parse(messageTemp);
  String status1 = (const char*)data1["statuss1"];
  String status2 = (const char*)data1["statuss2"];
  String status3 = (const char*)data1["statuss3"];
  String status4 = (const char*)data1["statuss4"];
  String status5 = (const char*)data1["statuss5"];
  
    if (status1 == "on1") {
      // Bật đèn 1
      digitalWrite(relay1D, HIGH);
    } else if (status1 == "off1") {
      // Tắt đèn 1
      digitalWrite(relay1D, LOW);
    }

        if (status2 == "on2") {
      // Bật đèn 2
      digitalWrite(relay2D, HIGH);
    } else if (status2 == "off2") {
      // Tắt đèn 2
      digitalWrite(relay2D, LOW);
    }

        if (status3 == "on3") {
      // Bật đèn 3
      digitalWrite(relay3D, HIGH);
    } else if (status3 == "off3") {
      // Tắt đèn 3
      digitalWrite(relay3D, LOW);
    }

        if (status4 == "on4") {
      // Bật đèn 4
      digitalWrite(relay4D, HIGH);
    } else if (status4 == "off4") {
      // Tắt đèn 4
      digitalWrite(relay4D, LOW);
    }

        if (status5 == "on5") {
      // Bật đèn 5
      digitalWrite(relay5wind, HIGH);
    } else if (status5 == "off5") {
      // Tắt đèn 5
      digitalWrite(relay5wind, LOW);
    }
}  
  Serial.println();
}
// ----------------------------------------------------------------------------------------------------------------------------------
//kết nối lại:
void reconnect() {
  // Loop until we're reconnected
  while (!clientP2.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (clientP2.connect("ESP8266Client")) {
      Serial.println("connected"); 
      clientP2.subscribe("#"); 
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
  pinMode(relay1D, OUTPUT);
  pinMode(relay2D, OUTPUT);
  pinMode(relay3D, OUTPUT);
  pinMode(relay4D, OUTPUT);
  pinMode(relay5wind, OUTPUT);
  dht.begin();
  Wire.begin(D1, D2); // Khởi tạo giao tiếp I2C
  lightMeter.begin(); // Khởi tạo cảm biến BH1750
  MQ135.setRegressionMethod(1); //_PPM =  a*ratio^b
  //MQ135.setA(102.2); MQ135.setB(-2.473); 
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
  clientP2.connect("ESP8266Client");
  MQ135.update();
  h = dht.readHumidity();
  h = round(h * 10)/10;
  t = dht.readTemperature();
  t = round(t * 10)/10;
  lux = lightMeter.readLightLevel();
  lux = round(lux * 10)/10;
  delay(20);
  MQ135.setA(102.2 ); MQ135.setB(-2.473); 
  float NH3 = MQ135.readSensor();
  NH3 = round(NH3 * 10)/10;
    delay(20);
  MQ135.setA(605.18); MQ135.setB(-3.937); 
  float CO = MQ135.readSensor(); 
  CO = round(CO * 10)/10;
    delay(20);
  MQ135.setA(77.255); MQ135.setB(-3.18); 
  float Alcohol = MQ135.readSensor(); 
  Alcohol = round(Alcohol * 10)/10;
    delay(20);
  MQ135.setA(110.47); MQ135.setB(-2.862); 
  float CO2 = MQ135.readSensor(); 
  CO2 = (round(CO2 * 10) / 10) + 400 ;
    delay(20);
// ----------------------------------------------------------------------------------------------------------------------------------
// sử lí chuỗi Json.
    data["phong2"] = phong2;
    data["temp2"] = t;
    data["humi2"] = h;
    data["Nh32"] = NH3;
    data["lux2"] = lux;
    data["2CO"] = CO;
    data["CO22"] = CO2;
    data["Alcoho2"] = Alcohol;
    String jsonString = JSON.stringify(data);
// ----------------------------------------------------------------------------------------------------------------------------------
// so sánh với giá trị cũ khi có giá trị mới rồi mới gửi.
  now = millis();
  // Publishes new temperature and humidity every 10 seconds
  if (now - lastMeasure > 10000) {
    lastMeasure = now;
    if(t != last_temp || h !=last_humi || NH3 != last_Nh3 || lux != last_lux || CO != last_CO || CO2 != last_CO2 || Alcohol !=last_Alcohol ){
      t = last_temp ;
      h = last_humi;
      NH3 = last_Nh3;
      lux = last_lux;
      CO = last_CO;
      CO2 = last_CO2;
      Alcohol = last_Alcohol;
      clientP2.publish("/PHONG2", jsonString.c_str());  
    }
  }
}