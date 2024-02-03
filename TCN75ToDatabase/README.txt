This program measures the temperature from two TCN75A thermometers
The thermometers are connected to an ESP32 using micropython
I2C kommunikation protocol is used to connect the thermometer and the microcontroller

Running the program UDPServerWClass.py sets up a python server with an UDPsocket
That recieves the two temperatures and saves them in a MySQL database