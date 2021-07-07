#include "DHT.h"
#include <SPI.h>
#include <Ethernet.h>


// assign a MAC address for the ethernet controller.
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
// Set the static IP address to use if the DHCP fails to assign
IPAddress ip(192, 168, 0, 177);
IPAddress myDns(192, 168, 0, 1);

// initialize the library instance:
EthernetClient client;

IPAddress server(3,137,144,214);

unsigned long lastConnectionTime = 0;           // last time you connected to the server, in milliseconds

const unsigned long postingInterval = 10*1000;  // delay between updates, in milliseconds


int PIR_PIN = 7;
int DHTPIN = 5;
const int SERVER_PORT = 5573;
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

int pirState = LOW;             
int motionDetected = 0;
float temperature = 0.0;
float humidity = 0.0;
String parsed;


void ethernetSetup() {
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // start the Ethernet connection:
  Serial.println("Initialize Ethernet with DHCP:");

  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");

    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
      while (true) {
        delay(1); // do nothing, no point running without Ethernet hardware
      }
    }

    if (Ethernet.linkStatus() == LinkOFF) {
      Serial.println("Ethernet cable is not connected.");
    }

    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip, myDns);
    Serial.print("My IP address: ");
    Serial.println(Ethernet.localIP());
  } else {
    Serial.print("  DHCP assigned IP ");
    Serial.println(Ethernet.localIP());
  }

  // give the Ethernet shield a second to initialize:
  delay(1000);
}



void setup() {
  pinMode(PIR_PIN, INPUT);
  dht.begin();
  Serial.begin(9600);
  // Initialize ethernet shield
  ethernetSetup();
}


void readMotion(){
  motionDetected = digitalRead(PIR_PIN);
  // Serial.println(motionDetected);
  if (motionDetected == HIGH) {            
    if (pirState == LOW) {
      Serial.println("Motion detected!");
      pirState = HIGH;
    }
  } else {
    if (pirState == HIGH){
      Serial.println("Motion ended!");
      pirState = LOW;
    }
  }
}


void readDht(){
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  humidity = dht.readHumidity();
  // Read temperature as Celsius (the default)
  temperature = dht.readTemperature();
  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.print(F("Humidity: "));
  Serial.print(humidity);
  Serial.print(F("%  Temperature: "));
  Serial.print(temperature);
  Serial.println(F("°C "));
}


// this method makes a HTTP connection to the server:
void httpRequest() {
  // close any connection before send a new request. This will free the socket on the WiFi shield

  client.stop();

  // if there's a successful connection:
  if (client.connect(server, SERVER_PORT)) {
    Serial.println("connecting...");
    // send the HTTP GET request:
    parsed = "GET /log-temp-hum-mot/" + String(temperature) + "/" + String(humidity) + "/" + String(motionDetected) + "/" + " HTTP/1.1";
    Serial.println(parsed);
    client.println(parsed);
    delay(3000);
    
    client.println("Host: 3.137.144.214");
    client.println("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36");
    client.println("Connection: close");
    client.println();

    // note the time that the connection was made:
    lastConnectionTime = millis();
  } else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
  }
}

void loop(){
  // Update motion sensor data
  readMotion();
  // Update temp and humidity data
  readDht(); 
  
  // if there's incoming data from the net connection. send it out the serial port.  This is for debugging purposes only:
  if (client.available()) {
    char c = client.read();
    Serial.write(c);
  }

  // if ten seconds have passed since your last connection, then connect again and send data:
  if (millis() - lastConnectionTime > postingInterval) {
    httpRequest();
  }
}
