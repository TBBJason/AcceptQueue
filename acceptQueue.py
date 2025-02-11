import win32serviceutil
import win32service
import win32event
import threading
import time
import pyautogui


class QueueAcceptService(win32serviceutil.ServiceFramework):
    _svc_name_ = "QueueAcceptService"
    _svc_display_name_ = "Queue Accept Service"
    _svc_description_ = "A service that automatically accepts queue for League/TFT"

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True
        self.thread = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_alive = False  # Signal the thread to stop
        win32event.SetEvent(self.hWaitStop)  # Trigger the stop event

        if self.thread and self.thread.is_alive():
            self.thread.join()  # Wait for the thread to exit

        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)  # Notify Windows that the service is running

        # Start the thread that runs the autoAccept function
        self.thread = threading.Thread(target=self.run_queue_accept)
        self.thread.start()

        # Wait for the stop event to be triggered
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def run_queue_accept(self):
        """Wrapper function to run autoAccept and ensure it stops gracefully."""
        while self.is_alive:
            try:
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
    win32serviceutil.HandleCommandLine(QueueAcceptService)