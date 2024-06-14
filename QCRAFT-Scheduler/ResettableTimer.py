from threading import Timer, Lock
import threading

class ResettableTimer:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.timer = Timer(self.timeout, self.callback_wrapper)
        self.lock = Lock()

    def callback_wrapper(self):
        self.callback()
        self.reset()

    def start(self):
        with self.lock:
            if not self.timer.is_alive():
                self.timer.start()

    def reset(self):
        with self.lock:
            if self.timer.is_alive():
                self.timer.cancel()
            self.timer = Timer(self.timeout, self.callback_wrapper)
            self.timer.start()

    def execute_and_reset(self):
        with self.lock:
            if self.timer.is_alive():
                threading.Thread(target=self.callback_wrapper).start()

    def stop(self):
        with self.lock:
            if self.timer.is_alive():
                self.timer.cancel()

    def is_alive(self):
        return self.timer.is_alive()