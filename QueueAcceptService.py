import win32serviceutil
import win32service
import win32event
import servicemanager
import time
import pyautogui
import logging
import os

class QueueAcceptService(win32serviceutil.ServiceFramework):
    _svc_name_ = "QueueAcceptService"
    _svc_display_name_ = "Queue Accept Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True

    def SvcStop(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              ("Service is stopping...", ''))
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        image_path = os.path.join(os.path.dirname(__file__), 'acceptqueue.png')
        acceptbutton = pyautogui.locateOnScreen(image_path, confidence=0.7)
        while self.is_alive:
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STARTED,
                                  (acceptbutton, ''))
            # win32event.WaitForSingleObject(self.hWaitStop, 5000)  # Wait for 5 seconds or stop signal
            # try:
            
            if acceptbutton:
                servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                servicemanager.PYS_SERVICE_STARTED,
                                ("INSIDE STATEMENT", ''))
                button_center = pyautogui.center(acceptbutton)
                pyautogui.click(button_center.x, button_center.y)
                logging.info("Queue accepted successfully")
                time.sleep(15)
            else:
                time.sleep(8) 
            # except Exception as e:
            #     logging.error(f"Error encountered: {str(e)}")
            #     time.sleep(10) 


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(QueueAcceptService)


# import win32serviceutil
# import win32service
# import win32event
# import threading
# import time
# import pyautogui
# import os
# import logging
# import servicemanager

# # Configure Logging
# logging.basicConfig(
#     filename=os.path.join(os.environ['SystemDrive'], 'QueueAcceptService.log'),
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# class QueueAcceptService(win32serviceutil.ServiceFramework):
#     _svc_name_ = "QueueAcceptService"
#     _svc_display_name_ = "Queue Accept Service"
#     _svc_description_ = "A service that automatically accepts queue for League/TFT"

#     def __init__(self, args):
#         win32serviceutil.ServiceFramework.__init__(self, args)
#         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
#         self.is_alive = True
#         self.thread = None

#     def SvcStop(self):
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         win32event.SetEvent(self.hWaitStop)  
#         self.is_alive = False  
        

#         if self.thread and self.thread.is_alive():
#             self.thread.join()  
#         self.ReportServiceStatus(win32service.SERVICE_STOPPED)


#     def SvcDoRun(self):
#         self.ReportServiceStatus(win32service.SERVICE_RUNNING)  

#         self.thread = threading.Thread(target=self.run_queue_accept)
#         self.thread.start()

#         win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

#     def run_queue_accept(self):
#         image_path = os.path.join(os.path.dirname(__file__), 'acceptqueue.png')
#         logging.info("Service started. Monitoring for queue accept...")
#         print("I'M GONNA KILL MYSELF")
#         print(self.is_alive)
#         while self.is_alive:
#             servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                                   servicemanager.PYS_SERVICE_STARTED,
#                                   ("Service is running...", ''))
#             win32event.WaitForSingleObject(self.hWaitStop, 5000)  # Wait for 5 seconds or stop signal
            # try:
            #     print("Checking for Accept Button")
            #     acceptbutton = pyautogui.locateOnScreen(image_path, confidence=0.7)
            #     print(acceptbutton)
            #     if acceptbutton:
            #         button_center = pyautogui.center(acceptbutton)
            #         pyautogui.click(button_center.x, button_center.y)
            #         logging.info("Queue accepted successfully")
            #         time.sleep(15)
            #     else:
            #         time.sleep(8) 
            # except Exception as e:
            #     logging.error(f"Error encountered: {str(e)}")
            #     time.sleep(10) 


# if __name__ == "__main__":
#     print("WHY ISN'T THIS WORKIGN")
#     win32serviceutil.HandleCommandLine(QueueAcceptService)
#     print("KILL YOURSELF")