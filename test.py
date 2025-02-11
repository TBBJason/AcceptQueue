import pyautogui
import time    

def run_queue_accept():
        """Wrapper function to run autoAccept and ensure it stops gracefully."""
        while True:
            try:
                print("Looking for game")
                # Look for the image on the screen
                acceptbutton = pyautogui.locateOnScreen('acceptqueue.png', confidence=0.7)
                print(acceptbutton)
                if acceptbutton:
                    # Get the center of the image
                    button_center = pyautogui.center(acceptbutton)
                    # Click the center of the image
                    pyautogui.click(button_center.x, button_center.y)
                    print("queue accepted")
                    time.sleep(15)  # Wait after accepting the queue
                else:
                    time.sleep(8)  # Wait before trying again
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)  # Wait before retrying after an error
if __name__ == "__main__":
     run_queue_accept()