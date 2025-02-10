import pyautogui
import time


def acceptQueue():
    while True:
        print("trying to find")
        try:
            # Look for the image on the screen
            acceptbutton = pyautogui.locateOnScreen('acceptqueue.png', confidence=0.7)
            print(acceptbutton)
            if acceptbutton:
                # Get the cnenter of the image
                button_center = pyautogui.center(acceptbutton)
                # Click the center of the image
                pyautogui.click(button_center.x, button_center.y)
                print("queue accepted")
                time.sleep(15)
            else:
                time.sleep(8)
        except Exception as e:
            time.sleep(10)


if __name__ == "__main__":
    acceptQueue()
