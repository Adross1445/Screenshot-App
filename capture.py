import time
import pyscreenshot as ImageGrab 
import schedule 
from datetime import datetime 
import pika
import subprocess
import os

def screenshot_to_queue(filepath):
    """
    Sends the screenshot file path to the RabbitMQ queue.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declares the queue
    channel.queue_declare(queue='screenshot_queue')

    # Publishes the file path
    channel.basic_publish(exchange='', routing_key='screenshot_queue', body=filepath)
    print(f"Sent {filepath} to queue.")

    connection.close()

def take_screen_shot():
    """
    Takes a screenshot and sends the file path to RabbitMQ
    """
    print("Taking screenshot...") 
    # Generates the image "screenshot-date&time of capture" and path
    image_name = f"screenshot-{str(datetime.now())}" 
    filepath = f"./Screenshots/{image_name}.png"
    
    # Captures and saves the screenshot
    screenshot = ImageGrab.grab()
    screenshot.save(filepath)
    print("Screenshot taken.")

    # Sends the file path to RabbitMQ
    screenshot_to_queue(filepath)

    # Opens the GUI to display the screenshot
    open_gui()

    return filepath


def open_gui():
    """
    Opens the GUI to display the screenshot.
    """
    gui_path = os.path.join(os.getcwd(), "gui.py")
    try:
        print(f"Opening GUI: {gui_path}")
        subprocess.Popen(["python", gui_path])
    except Exception as e:
        print(f"Failed to open GUI: {e}")

def main():
    """
    Schedules a screenshot to be taken every hour and to pause for 1
    second to allow it to start again.
    """
    # Takes the screenshot every hour.
    schedule.every().hour.do(take_screen_shot)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    import os
    os.makedirs('./Screenshots', exist_ok=True)

    # Takes a screenshot when the script starts to verify its running.
    take_screen_shot()
    
    main()