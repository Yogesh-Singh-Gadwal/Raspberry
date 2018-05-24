import wiringpi
import time
import os
 
wiringpi.wiringPiSetupSys()
 
os.system('gpio export 17 out')
 
wiringpi.pinMode(17,1)
 
while True:
    time.sleep(0.5)
    wiringpi.digitalWrite(17,1)
    time.sleep(0.5)
    wiringpi.digitalWrite(17,0)
