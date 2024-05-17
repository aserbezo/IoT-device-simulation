import json
import time
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from datetime import datetime
import random
# Open the JSON file
with open('sofia-burgas-route.json', 'rb') as file:
    # Load the JSON data from the file
    decoded_content = file.read().decode('utf-8')

# loaded data
data = json.loads(decoded_content)
# between 75 to 105 degrees Celsius
speed = [60,64,65,68,70,75,77,74,80,82,88,85,81,90,92,94,96,97,95,100,111,104,105,110,120,150,160]
temp = [75, 80 ,90,100,76,90,100,110,115,130,77,83]
alert = ['None','Battery Charge Warning Light','Oil Pressure Warning Light','Brake Warning Light','Transmission Temperature','None','None','None','None']
#  Normal 30 to 35 PSI
tire_pressure = [30,31,32,33,29,25]

async def send_message_to_iot_hub(conn_str, message_content):
    try:
        # Create an instance of the IoT Hub device client
        client = IoTHubDeviceClient.create_from_connection_string(conn_str)

        if client is None:
            raise Exception("Failed to create IoT Hub device client.")

        # Connect the client to the IoT Hub
        await client.connect()

        # Create a Message object with the message content
        message = Message(json.dumps(message_content))

        # Send the message
        await client.send_message(message)
        print("Message sent to Azure IoT Hub:", message_content)

    except Exception as e:
        print("Error:", e)

    finally:
        # Disconnect the client
        if client:
            await client.disconnect()


# Define the connection string and message content
connection_string = ""

# Call the asynchronous function to send the message
for value in data.values():
    for i in value:
        Latitude = i[0]
        Longitude = i[1]
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        curr_temp = random.choice(temp)
        curr_speed = random.choice(speed)
        curr_tire_pressure = random.choice(tire_pressure)
        curr_alet = random.choice(alert)
        message_content = {'DeviceId': 1112222333,
                           'Latitude': Latitude,
                           'Longitude': Longitude,
                           'time':current_time,
                           'temp': curr_temp,
                           'tire_press': curr_tire_pressure,
                           'speed':curr_speed,
                           'alert':curr_alet}
        asyncio.run(send_message_to_iot_hub(connection_string, message_content))
        time.sleep(10)  # Adjust for faster/slower update frequency


