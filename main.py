import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from  azure.iot.device import Message


async def send_message_to_iot_hub(conn_str, message_content):
    try:
        # Create an instance of the IoT Hub device client
        client = IoTHubDeviceClient.create_from_connection_string(conn_str)

        if client is None:
            raise Exception("Failed to create IoT Hub device client.")

        # Connect the client to the IoT Hub
        await client.connect()

        # Create a Message object with the message content
        message = Message(message_content)

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
connection_string = "Your Conn string"
message_content = "Hello from Azure IoT!"

# Call the asynchronous function to send the message
asyncio.run(send_message_to_iot_hub(connection_string, message_content))
