#include <SPI.h>
#include <Ethernet.h>

// assign a MAC address for the ethernet controller.
// fill in your address here:
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
// Set the static IP address to use if the DHCP fails to assign

IPAddress ip(192, 168, 0, 177);

IPAddress myDns(192, 168, 0, 1);

// initialize the library instance:

EthernetClient client;

// char server[] = "www.arduino.cc";  // also change the Host line in httpRequest()
IPAddress server(3,137,144,214);

unsigned long lastConnectionTime = 0;           // last time you connected to the server, in milliseconds

const unsigned long postingInterval = 10*1000;  // delay between updates, in milliseconds

int cntr = 1;
String url;
int temp;
int hum;
boolean mot = false;


void setup() {

  // You can use Ethernet.init(pin) to configure the CS pin

  //Ethernet.init(10);  // Most Arduino shields

  //Ethernet.init(5);   // MKR ETH shield

  //Ethernet.init(0);   // Teensy 2.0

  //Ethernet.init(20);  // Teensy++ 2.0

  //Ethernet.init(15);  // ESP8266 with Adafruit Featherwing Ethernet

  //Ethernet.init(33);  // ESP32 with Adafruit Featherwing Ethernet

  // start serial port:

  Serial.begin(9600);

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

void loop() {

  // if there's incoming data from the net connection.

  // send it out the serial port.  This is for debugging

  // purposes only:

  if (client.available()) {

    char c = client.read();

    Serial.write(c);

  }

  // if ten seconds have passed since your last connection,

  // then connect again and send data:

  if (millis() - lastConnectionTime > postingInterval) {

    httpRequest();

  }

}

// this method makes a HTTP connection to the server:
void httpRequest() {

  // close any connection before send a new request.

  // This will free the socket on the WiFi shield

  client.stop();

  // if there's a successful connection:

  if (client.connect(server, 5573)) {

    Serial.println("connecting...");

    // send the HTTP GET request:
    temp = cntr + 5;
    hum = cntr + 1;
    if (cntr % 2 == 0){
      mot = true;
    } else {
      mot = false;
    }
    
    url = "GET /log-temp-hum-mot/" + String(temp) + "/" + String(hum) + "/" + String(mot) + "/" + " HTTP/1.1";
    Serial.println(url);
    client.println(url);
    delay(3000);
//    client.println("GET /l-stat-api/ HTTP/1.1");
    
    cntr += 1;
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
