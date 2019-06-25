#include <Keyboard.h>

void setup() {
  // put your setup code here, to run once:
  Keyboard.begin();

  delay(1000);

  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  delay(10);
  Keyboard.releaseAll();

  delay(200);

  Keyboard.print("cmd");

  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();

  delay(1000);
  
  Keyboard.print("Fuck you");
}

void loop() {
  // put your main code here, to run repeatedly:

}
