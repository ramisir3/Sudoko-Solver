#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include <ArduinoJson.h>
#include <SoftwareSerial.h>



//connect raspberry to  serial0:
#define RXD0 3
#define TXD0 1
#define PiSerial Serial
const char* ssid = "APESP";
const char* password =  "123456780";


AsyncWebServer server(80);

bool raspBusy = false;

int operating_mode;
int level;
const char* values;
String val;

int callMain = 0;

void setup() {
  PiSerial.begin(9600);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  //get object from mobile
  server.on(
    "/post",
    HTTP_POST,
  [](AsyncWebServerRequest * request) {},
  NULL,
  [](AsyncWebServerRequest * request, uint8_t *data, size_t len, size_t index, size_t total) {


    StaticJsonDocument<192> doc;

    DeserializationError error = deserializeJson(doc, data, len);

    if (error) {
      Serial.print("deserializeJson() failed: ");
      Serial.println(error.c_str());
      return;
    }

    operating_mode = doc["mode"];
    level = doc["level"];
    values = doc["values"];

    if (raspBusy) {
      request->send(404, "application/json", "{\"result\":\"Raspberry Busy\"}" );
    } else {
      callMain = 1;
      request->send(200, "application/json", "{\"result\":\"Operate successfully\"}" );
    }
  });


  server.on(
    "/values",
    HTTP_GET,
  [](AsyncWebServerRequest * request) {

    raspberryRead();
    //get from raspberry
    StaticJsonDocument<128> doc;

    doc["values"] = val;
    String s = "";
    serializeJson(doc, s);
    request->send(200, "application/json", s);

  },
  NULL,
  [](AsyncWebServerRequest * request, uint8_t *data, size_t len, size_t index, size_t total) {});


  server.begin();
}


//receive from Raspberry
void raspberryRead() {
  raspBusy = true;
  PiSerial.print(1);
  while (PiSerial.available()  <= 0) {  }
  val = Serial.readString();
  raspBusy = false;
}


//send to Raspberry
void sendToRaspberry() {
  raspBusy = true;
  if (operating_mode == 0) {
    //take image
    PiSerial.print(operating_mode);
    while (PiSerial.available()  <= 0) {  }
    PiSerial.read();
    raspBusy = false;
  } else if (operating_mode == 1) {
    //send user grid
    PiSerial.print(3);
    while (PiSerial.available()  <= 0) {  }
    PiSerial.read();
    PiSerial.print(values);
    while (PiSerial.available()  <= 0) {  }
    PiSerial.read();
    raspBusy = false;
  } else if (operating_mode == 2) {
    // send level
    PiSerial.print(operating_mode);
    while (PiSerial.available()  <= 0) {  }
    PiSerial.read();
    PiSerial.print(level);
    while (PiSerial.available()  <= 0) {  }
    PiSerial.read();
    raspBusy = false;
  }
}

void loop() {
  vTaskDelay(10);
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.disconnect();
    delay(100);
    WiFi.begin(ssid, password);
  }
  if (!raspBusy && callMain == 1) {
    raspBusy = true;
    sendToRaspberry();
    callMain = 0;
    raspBusy = false;
  }
}
