from azure.servicebus import ServiceBusClient, ServiceBusMessage


class ServiceBusConnector:
    def __init__(self, connection_string: str):
        self.client = ServiceBusClient.from_connection_string(connection_string)

    def send_message(self, topic_name: str, message: str):
        sender = self.client.get_topic_sender(topic_name=topic_name)
        sender.send_messages(ServiceBusMessage(message))

    def close_connection(self):
        self.client.close()
