import tkinter as tk
from PIL import Image, ImageTk
import pika
import threading
import os


def display_image(filepath):
    """
    Displays the image stretched to fill the fixed window size.
    """
    global current_image

    # Checks if the file exists
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return

    img = Image.open(filepath)

    # Resizes the image to fill the fixed window size
    img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)

    # Converts the image to a format compatible with Tkinter
    current_image = ImageTk.PhotoImage(img)

    # Updates the label to display the image
    image_label.config(image=current_image)
    image_label.image = current_image  # Keep a reference to prevent garbage collection
    print(f"Image displayed at {WINDOW_WIDTH}x{WINDOW_HEIGHT}.")


def on_message(ch, method, properties, body):
    """
    Callback to handle messages received from RabbitMQ.
    """
    filepath = body.decode('utf-8')
    print(f"Received file path from RabbitMQ: {filepath}")
    root.after(0, display_image, filepath)


def setup_rabbitmq_consumer():
    """
    Sets up RabbitMQ consumer to listen for new screenshots.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declares the queue
    channel.queue_declare(queue='screenshot_queue')

    # Sets up the consumer
    channel.basic_consume(queue='screenshot_queue', on_message_callback=on_message, auto_ack=True)
    print("Waiting for messages from RabbitMQ...")
    channel.start_consuming()


# Constants for window size
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Creates the main Tkinter window
root = tk.Tk()
root.title("Screenshot Viewer")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")  # Set window size
root.resizable(False, False)  # Disable resizing

# Creates a label to display the image
image_label = tk.Label(root, bg="black")
image_label.pack(fill=tk.BOTH, expand=True)

# Starts RabbitMQ consumer in a separate thread
consumer_thread = threading.Thread(target=setup_rabbitmq_consumer, daemon=True)
consumer_thread.start()

# Runs the Tkinter main loop
root.mainloop()



