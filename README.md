# Screenshot Viewer with RabbitMQ

This project is a Python application that captures screenshots on a schedule, sends the file paths to a RabbitMQ queue, and displays the screenshots dynamically in a GUI. It demonstrates how to use RabbitMQ for communication between a producer (`capture.py`) and a consumer (`gui.py`) while providing a simple and user-friendly interface.

---

## Features

- **Scheduled Screenshots**: Automatically captures screenshots using `capture.py`.
- **RabbitMQ Integration**: Communicates file paths between the producer and consumer via a RabbitMQ queue.
- **Dynamic Image Display**: Displays screenshots in a Tkinter-based GUI with a static window size.
- **Simple Workflow**: Decouples the screenshot capture process and the image viewer.

---

## Requirements

Before running this project, ensure you have the following installed:

- **Python 3.8+**
- **RabbitMQ Server** (Make sure RabbitMQ is running locally)
- Required Python libraries (see below)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Adross1445/Screenshot-App
   cd Screenshot-App

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
4. Ensure RabbitMQ is installed and running locally:
   ```bash
   sudo service rabbitmq-server start

---

## Usage 
1. Start the GUI
   Run the gui.py script to start the image viewer and listen for messages from RabbitMQ:
   ```bash
   python gui.py
2. Capture a Screenshot
   Run the capture.py script to capture a screenshot and send its file path to    RabbitMQ:
   ```bash
   python capture.py
   The captured screenshot will be saved in the Screenshots folder and displayed in the GUI.
   
---

## File Structure

- **Screenshot-App/**
  - `capture.py`: Captures screenshots and sends file paths to RabbitMQ.
  - `gui.py`: Displays screenshots received from RabbitMQ.
  - `Screenshots/`: Directory where screenshots are saved.
  - `requirements.txt`: List of required Python libraries.
  - `.gitignore`: Git ignore file for excluding unnecessary files.
  - `README.md`: Project documentation.

---

## Configuration
- Window Size: The GUI window is set to a fixed size of 1200x800 in gui.py. You can adjust this by changing the WINDOW_WIDTH and WINDOW_HEIGHT constants in the script.
- RabbitMQ Queue: The queue name is set to screenshot_queue. This can be changed in both capture.py and gui.py.

---

## Troubleshooting
1. RabbitMQ Not Running: Ensure RabbitMQ is installed and running locally:
   ```bash
   sudo service rabbitmq-server start
2. GUI Not Opening: 
   Check the terminal output for any errors. Ensure gui.py is running properly and RabbitMQ is configured correctly.
3. Missing Screenshots: 
   Ensure the Screenshots directory exists. If not, it will be created automatically by capture.py.
   
---

## Future Improvements
- Add support for resizing the GUI dynamically.
- Enable screenshot preview thumbnails in the GUI.
- Enhance error handling for RabbitMQ connectivity issues.

---

## License
This project is open-source and available under the MIT License.
