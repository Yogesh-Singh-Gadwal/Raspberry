import asyncio
import datetime
import random
import websockets
import wiringpi
import time
import os
import Adafruit_DHT     #for DHT11 sensor

#settingup the wiringPI
wiringpi.wiringPiSetupSys()

#putting 17th gpio to out mode
os.system('gpio export 17 out')

#making the selected pin high as default
wiringpi.pinMode(17,1)


#for dht11 sensor start
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
gpio=27
#sensor end

async def time(websocket, path):
    while True:
        #data=await websocket.recv()
        # Use read_retry method. This will retry up to 15 times to
        # get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        #formatting and converting temp and hum data into an string
        sensordata='Humidity = '+str(humidity)+' Temperature = '+str(temperature)
        print(sensordata) #printing to the console just to check
        

        #getting time data and formatting
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        #concatting timne and the sensor data
        x=now+sensordata
        #sending data to web using websocket
        await websocket.send(x)
        await asyncio.sleep(random.random() * 3)
        
        #recieving data to set thresold value
        threshold=await websocket.recv()

        #controlling led with threshold value
        if(temperature>threshold):
            wiringpi.digitalWrite(17,1)
        if(temperature<=threshold):
            wiringpi.digitalWrite(17,0)

            

start_server = websockets.serve(time, '127.0.0.1', 12361)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
 
