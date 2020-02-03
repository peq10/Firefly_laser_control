void setup()

{

pinMode(LED_BUILTIN, OUTPUT);

Serial.begin(9600);

while (!Serial);

Serial.println("Input 1 to Turn LED on and 2 to off");

}

void loop() {

if (Serial.available())

{

int state = Serial.parseInt();

if (state == 1)

{

digitalWrite(LED_BUILTIN, HIGH);

Serial.println("Command completed LED turned ON");

}

if (state == 0)

{

digitalWrite(LED_BUILTIN, LOW);

Serial.println("Command completed LED turned OFF");

}

}

}
