import pika
import time
from mss import mss
import uuid

# RabbitMQ configuration constants
EXCHANGE = 'screenshot_exchange'
REQUEST_QUEUE = 'screenshot_requests'
DATA_QUEUE = 'screenshot_data'

# Establish RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Ensure queue existence
channel.queue_declare(queue=REQUEST_QUEUE)

# Graceful shutdown flag
running = True

def capture_screenshot():
    """Captures a screenshot and saves it to a temporary file.

    Returns:
        str: Path to the saved screenshot file.
    """
    with mss() as sct:
        # Generate a unique file path for the screenshot
        file_path = f"/tmp/{uuid.uuid4()}.png"
        sct.shot(output=file_path)
        print(f"Screenshot saved to {file_path}")
        return file_path

def handle_request(ch, method, properties, body):
    """Callback function to handle incoming screenshot requests.

    Captures a screenshot and publishes it to the screenshot data queue.
    """
    print("Received screenshot request.")
    # Capture the screenshot
    file_path = capture_screenshot()
    with open(file_path, 'rb') as f:
        # Read the screenshot file as binary data
        screenshot_data = f.read()
    # Publish the screenshot data to the RabbitMQ queue
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key='data',
        body=screenshot_data
    )
    print("Screenshot sent.")

def shutdown():
    """Cleans up and closes RabbitMQ connection on shutdown."""
    print("Shutting down screenshot service...")
    global running
    running = False
    if connection and connection.is_open:
        connection.close()

# Set up consumer to listen for screenshot requests
channel.basic_consume(queue=REQUEST_QUEUE, on_message_callback=handle_request, auto_ack=True)

try:
    print("Waiting for screenshot requests...")
    while running:
        connection.process_data_events(time_limit=1)
except KeyboardInterrupt:
    shutdown()