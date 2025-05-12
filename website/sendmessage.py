import asyncio
import os
from dotenv import load_dotenv
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage

load_dotenv()

QUEUE_NAME = os.environ.get("DJANGO_QUEUE")
connection_string = os.environ.get("CONNECTION_STRING")


async def send_single_message(order_json):
    # create a Service Bus client using the credential
    async with ServiceBusClient.from_connection_string(connection_string) as servicebus_client:
        # get a Queue Sender object to send messages to the queue
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        async with sender:
    # Create a Service Bus message and send it to the queue
            message = ServiceBusMessage(order_json)
            await sender.send_messages(message)
            print("Sent a single message")


