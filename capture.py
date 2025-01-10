import time

import pyscreenshot as ImageGrab 
import schedule 


from datetime import datetime 


def take_screen_shot():
    print("Taking screenshot...")
    image_name = f"screenshot-{str(datetime.now())}"
    screenshot = ImageGrab.grab()

    filepath = f"./Screenshots/{image_name}.png"
 
    screenshot.save(filepath)

    print("Screenshot taken.")

    return filepath

def main():
    schedule.every(1).hour.do(take_screen_shot)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
