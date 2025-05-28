#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN   9    // Define reset pin
#define SS_PIN    10   // Define slave select pin

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance



void setup() {
    Serial.begin(9600);
    Serial.println("serial initialized");
    delay(5000);
    //mfrc522.PCD_Init();   // Initialize MFRC522
    

    bool initializationSuccessful = false;
    while (!initializationSuccessful) {
        mfrc522.PCD_Init();
        if (mfrc522.PCD_PerformSelfTest()) {
            initializationSuccessful = true;
            Serial.println("MFRC522 initialized successfully!");
        } else {
            Serial.println("MFRC522 initialization failed! Retrying...");
            delay(1000); // Wait for 1 second before retrying
        }
    }

    Serial.println("setup complete");
}



void loop() {
    //Serial.println("Hello from Arduino!"); // Send data over serial port
    delay(1000); // Wait for 1 second
    bool initializationSuccessful2 = mfrc522.PCD_PerformSelfTest();
    if (!initializationSuccessful2) {
        mfrc522.PCD_Init();
        Serial.println("retrying...");
    }
    // Check if a card is present
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
        // Card detected, read UID
        Serial.print("UID:");
        for (byte i = 0; i < mfrc522.uid.size; i++) {
            //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
            Serial.print(mfrc522.uid.uidByte[i], HEX);
        }
        Serial.println();

        mfrc522.PICC_HaltA();  // Halt PICC
        mfrc522.PCD_StopCrypto1(); // Stop encryption on PCD
    }
}
