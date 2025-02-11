import win32serviceutil
import win32service
import win32event
import threading
import time
import acceptQueue  # Import correctly

class QueueAcceptService(win32serviceutil.ServiceFramework):  # Renamed to avoid conflict
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
        self.is_alive = False
        acceptQueue.stop()  # Stop the `autoAccept` loop
        win32event.SetEvent(self.hWaitStop)

        if self.thread and self.thread.is_alive():
            self.thread.join()  # Wait for thread to exit

        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)  # Notify Windows that service is running

        self.thread = threading.Thread(target=self.run_queue_accept)
        self.thread.start()

        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def run_queue_accept(self):
        """Wrapper function to run autoAccept and ensure it stops gracefully."""
        while self.is_alive:
            acceptQueue.autoAccept()  
            time.sleep(1)  # Prevent CPU overuse

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(QueueAcceptService)



# import win32serviceutil
# import win32service
# import win32event
# import threading
# import time
# import acceptQueue  # Import correctly

# class QueueAcceptService(win32serviceutil.ServiceFramework):  # Renamed to avoid conflict
#     _svc_name_ = "QueueAcceptService"
#     _svc_display_name_ = "Queue Accept Service"
#     _svc_description_ = "A service that automatically accepts queue for League/TFT"

#     def __init__(self, args):
#         super().__init__(args)
#         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
#         self.is_alive = True
#         self.thread = None  

#     def SvcStop(self):
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         self.is_alive = False
#         acceptQueue.stop()  # Stop the `autoAccept` loop
#         win32event.SetEvent(self.hWaitStop)

#         if self.thread and self.thread.is_alive():
#             self.thread.join()  # Wait for thread to exit

#         self.ReportServiceStatus(win32service.SERVICE_STOPPED)

#     def SvcDoRun(self):
#         self.ReportServiceStatus(win32service.SERVICE_RUNNING)  # Notify Windows that service is running

#         self.thread = threading.Thread(target=self.run_queue_accept)
#         self.thread.start()

#         win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

#     def run_queue_accept(self):
#         """Wrapper function to run autoAccept and ensure it stops gracefully."""
#         while self.is_alive:
#             acceptQueue.autoAccept()  
#             time.sleep(1)  # Prevent CPU overuse

# if __name__ == "__main__":
#     win32serviceutil.HandleCommandLine(QueueAcceptService)
