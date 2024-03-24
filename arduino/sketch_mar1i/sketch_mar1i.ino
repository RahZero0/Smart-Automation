#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Wifi _ username";  // Your WiFi SSID
const char* password = "*********";     // Your WiFi password

// Define the pin numbers for the traffic lights
const int redPins[] = {2, 12, 19, 23};
const int orangePins[] = {4, 13, 21, 25};
const int greenPins[] = {5, 18, 22, 27};

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  delay(1000);

  // Connect to WiFi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Initialize the pin modes for all lights
  for (int i = 0; i < 4; i++) {
    pinMode(redPins[i], OUTPUT);
    pinMode(orangePins[i], OUTPUT);
    pinMode(greenPins[i], OUTPUT);
  }
}

///
void loop() {
  int i = 0;
  controlTrafficLights(i);
  i = i + 1;
}

void controlTrafficLights(int i) {
  
  int funbox = random(2, 5);
  if ( i < 1 ) {
    funbox = 4;
  }

  int numLights = funbox;

  HTTPClient http;

  String partial = "\"C:\\Users\\Ayush\\OneDrive\\Desktop\\trafficnetdatasetv1\\train\\densetraffic\\";

  String postData = "\"";

  for (int i = 0; i < funbox; i++) {
    int randomNumber = random(1, 901); // Random number between 1 and 900 (inclusive)
    String parttial ;
    parttial = partial + String(randomNumber) + ".jpg\"";
    if (i < funbox - 1) {
      parttial = parttial + ", ";
    }
    postData = postData + parttial;
  }
  postData = postData + "\"";
  Serial.println(postData);

  // Your server's URL
  const char* url = "http://192.168.39.76:5000/hello";

  // Set Content-Type header
  http.addHeader("Content-Type", "application/json");

  // Create JSON payload
  // postData = "\"C:\\Users\\Ayush\\OneDrive\\Documents\\GitHub\\Smart-Automation\\images\\ht1.img\", \"C:\\Users\\Ayush\\OneDrive\\Documents\\GitHub\\Smart-Automation\\images\\i1.webp\", \"C:\\Users\\Ayush\\OneDrive\\Documents\\GitHub\\Smart-Automation\\images\\i2.jpg\", \"C:\\Users\\Ayush\\OneDrive\\Documents\\GitHub\\Smart-Automation\\images\\i3\"";

  // Make a POST request
  http.begin(url);
  int httpResponseCode = http.POST(postData);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    // Print JSON response
    String payload = http.getString();
    Serial.println("Response:");
    Serial.println(payload);

    float numbers[funbox]; // Assuming there are 4 numbers

    // Find the position of '[' and ']'
    int startPos = payload.indexOf('[');
    int endPos = payload.indexOf(']');

    if (startPos != -1 && endPos != -1) {
      // Extract the substring between '[' and ']'
      String numbersStr = payload.substring(startPos + 1, endPos);

      // Split the string by comma and extract individual numbers
      int commaPos = 0;
      int index = 0;
      while (commaPos != -1) {
        commaPos = numbersStr.indexOf(',');
        if (commaPos != -1) {
          String numberStr = numbersStr.substring(0, commaPos);
          numbersStr = numbersStr.substring(commaPos + 1);
          // Convert string to float and store in the array
          numbers[index++] = numberStr.toFloat();
        }
      }
      // Store the last number after the last comma
      numbers[index] = numbersStr.toFloat();
    }

    for (int i = 0; i < numLights; i++) {
      digitalWrite(redPins[i], HIGH);
    }

    delay(2000);

    for (int i = 0; i < numLights; i++) {
      digitalWrite(redPins[i], LOW);
      digitalWrite(orangePins[i], HIGH);

      delay(4000);

      digitalWrite(orangePins[i], LOW);
      digitalWrite(greenPins[i], HIGH);

      delay(numbers[i]);

      digitalWrite(greenPins[i], LOW);
      digitalWrite(orangePins[i], HIGH);

      delay(4000);

      digitalWrite(orangePins[i], LOW);
      digitalWrite(redPins[i], HIGH);
    }
  } else {
    Serial.print("Error in HTTP request. HTTP Response code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}
