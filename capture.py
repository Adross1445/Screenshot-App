import time

import pyscreenshot as ImageGrab 
import schedule 

from datetime import datetime 


def take_screen_shot():
    """
    Takes a screenshot of the device's screens and sends it to the
    Screenshots folder located in the app folder. Also has text outout
    informing the user of the screenshot's status.
    """
    print("Taking screenshot...") 
    image_name = f"screenshot-{str(datetime.now())}" # Names the image "screenshot-date&time of capture".
    screenshot = ImageGrab.grab() # Module capturing the screenshot.

    filepath = f"./Screenshots/{image_name}.png" # Creates a variable of the screenshot's storage destination.
 
    screenshot.save(filepath) 

    print("Screenshot taken.")

    return filepath

def main():
    """
    Schedules a screenshot to be taken every hour and to pause for 1
    second to allow it to start again.
    """
    schedule.every(1).hour.do(take_screen_shot) # Takes the screenshot every hour.

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
