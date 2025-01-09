import pika

def setup_rabbitmq():
    """Sets up RabbitMQ with required queues and exchanges."""
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare exchange for routing messages between queues
    channel.exchange_declare(exchange='screenshot_exchange', exchange_type='direct')

    # Declare queues for screenshot requests and data
    channel.queue_declare(queue='screenshot_requests')
    channel.queue_declare(queue='screenshot_data')

    # Bind queues to exchange with appropriate routing keys
    channel.queue_bind(exchange='screenshot_exchange', queue='screenshot_requests', routing_key='request')
    channel.queue_bind(exchange='screenshot_exchange', queue='screenshot_data', routing_key='data')

    print("RabbitMQ setup complete.")
    connection.close()

if __name__ == "__main__":
    setup_rabbitmq()