from threading import Timer, Lock
import threading

class ResettableTimer:
    """
    A timer that can be reset

    Methods
    -------
    callback_wrapper()
        Wrapper for the callback function

    start()
        Start the timer

    reset()
        Reset the timer

    execute_and_reset()
        Execute the callback function and reset the timer

    stop()
        Stop the timer

    is_alive()
        Check if the timer is alive
    """
    def __init__(self, timeout, callback):
        """
        Initializes a new instance of the ResettableTimer class

        Attributes:
            timeout (int): The time to wait before executing the callback function
            callback (function): The function to execute when the timer expires            
            timer (Timer): The timer object            
            lock (Lock): The lock object
        """
        self.timeout = timeout
        self.callback = callback
        self.timer = Timer(self.timeout, self.callback_wrapper)
        self.lock = Lock()

    def callback_wrapper(self) -> None:
        """
        Wrapper for the callback function. It executes the callback function and resets the timer
        """
        self.callback()
        self.reset()

    def start(self) -> None:
        """
        Start the timer if it is not already running
        """
        with self.lock:
            if not self.timer.is_alive():
                self.timer.start()

    def reset(self) -> None:
        """
        Reset the timer if it is running
        """
        with self.lock:
            if self.timer.is_alive():
                self.timer.cancel()
            self.timer = Timer(self.timeout, self.callback_wrapper)
            self.timer.start()

    def execute_and_reset(self) -> None:
        """
        Execute the callback function and reset the timer
        """
        with self.lock:
            if self.timer.is_alive():
                threading.Thread(target=self.callback_wrapper).start()

    def stop(self) -> None:
        """
        Stop the timer if it is running
        """
        with self.lock:
            if self.timer.is_alive():
                self.timer.cancel()

    def is_alive(self) -> bool:
        """
        Check if the timer is alive

        Returns:
            bool: True if the timer is alive, False otherwise
        """
        return self.timer.is_alive()