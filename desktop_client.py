import pika
import os
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PIL import Image
from io import BytesIO

class ScreenshotViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.rabbitmq_connect()

    def init_ui(self):
        """Initializes the graphical user interface for the desktop client."""
        self.setWindowTitle("Screenshot Viewer")
        # Label to display screenshots or messages
        self.label = QLabel("No screenshots yet.", self)
        # Button to request a new screenshot
        self.request_button = QPushButton("Request Screenshot", self)
        self.request_button.clicked.connect(self.request_screenshot)
        # Layout to arrange widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.request_button)
        self.setLayout(layout)

    def rabbitmq_connect(self):
        """Connects to RabbitMQ and sets up a consumer to receive screenshot data."""
        # Establish connection to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        # Ensure the screenshot data queue exists
        self.channel.queue_declare(queue='screenshot_data')
        # Set up consumer to process incoming screenshots
        self.channel.basic_consume(queue='screenshot_data', on_message_callback=self.on_screenshot_received, auto_ack=True)
        print("Connected to RabbitMQ and waiting for screenshots.")

    def request_screenshot(self):
        """Sends a request to capture a screenshot via RabbitMQ."""
        # Create a new connection to send the request
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        # Publish the request to the screenshot requests queue
        channel.basic_publish(exchange='screenshot_exchange', routing_key='request', body='capture_now')
        print("Screenshot request sent.")
        connection.close()

    def on_screenshot_received(self, ch, method, properties, body):
        """Callback function to handle incoming screenshot data.

        Args:
            ch: Channel object.
            method: Method frame with delivery details.
            properties: Properties of the received message.
            body: Binary data of the received screenshot.
        """
        print("Screenshot received.")
        # Convert the binary data into an image
        image = Image.open(BytesIO(body))
        # Save the image locally
        file_path = "received_screenshot.png"
        image.save(file_path)
        print(f"Screenshot saved to {file_path}")
        # Update the UI with the new screenshot
        pixmap = QPixmap(file_path)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        """Handle application close event to clean up RabbitMQ connections."""
        print("Closing RabbitMQ connection...")
        if self.connection and self.connection.is_open:
            self.connection.close()
        event.accept()

if __name__ == "__main__":
    # Ensure PyQt uses the correct platform plugin
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication([])
    viewer = ScreenshotViewer()
    try:
        viewer.show()
        app.exec_()
    except KeyboardInterrupt:
        print("Application interrupted. Exiting...")
        viewer.close()


