from datetime import datetime
import time
import os

from pyvesync import VeSync
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(os.getenv("MQTT_SERVER"), 1883)
print("Connected to MQTT Broker.")

manager = VeSync(os.getenv("USERNAME"), os.getenv("PASSWORD"), "GMT", debug=False, redact=True)
manager.login()

manager.update()

client.loop_start()

switch = manager.device_list[0]
#f = open("power.csv", "a") # 0 for unbuffered writing
#f.write("date,power,voltage,current,energy\n")
# switch.display()
while True:
  switch.update()

  power = int(switch.power)
  energy = int(switch.energy_today * 1000)
  print(f"{power} W, {energy} Wh", flush=True)
  dt = datetime.now()
  ts = datetime.timestamp(dt)
  client.publish("testsensor/power", power)
  client.publish("testsensor/energy", energy)
  # client.loop()
  #f.write(f"{int(ts)},{switch.power},{switch.voltage},{switch.current},{switch.energy_today}\n")
  #f.flush()
  # switch.energy needs to be read out or calculated somehow…
  time.sleep(30)

#f.close()
client.loop_stop()


# watch -n 10 "cut -d ',' -f 2 power.csv | tail -n 150 | plot -b 0:500 -d 40:150"
