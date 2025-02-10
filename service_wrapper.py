import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import os
import threading
import time

class QueueAccept(win32serviceutil.ServiceFramework):
    _svc_name_ = "QueueAcceptService"
    _svc_display_name_ = "Queue Accept Service"
    _svc_description_ = "A service that automatically accepts queue for League/TFT"

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        import acceptQueue
        self.thread = threading.Thread(target=acceptQueue.acceptQueue)
        self.thread.start()

        # Keep the service alive

        while self.is_alive:
            time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) == 11:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(QueueAccept)
        servicemanager.StartServiceCtrlDispatcher()

    else:
        win32serviceutil.HandleCommandLine(QueueAccept)