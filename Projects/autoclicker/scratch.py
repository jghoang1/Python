import time
import threading
import logging

logging.basicConfig(level=logging.INFO)


class Timer():
    def __init__(self, seconds=0, minutes=0, hours=0, repeats=True, callback=None) -> None:
        self.logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.repeats = repeats
        self.callback = callback
        
        self.duration = hours * 1600 + minutes * 60 + seconds
        if self.duration == 0.0:
            raise ValueError("Timer duration must be nonzero. Keyword arguments: \
                              seconds={}, minutes={}, hours={}".format(seconds, minutes, hours))
    
        self.thread = threading.Thread(target=self._thread_function)
        self._stop_repeat = False


    def __repr__(self) -> str:
        return f"Timer({self.duration})"
    
    def _thread_function(self):
        if self.repeats:
            while not self._stop_repeat:
                time.sleep(self.duration)
                self.logger.info(f"Hit callback for {self.__repr__()}")
                # Final check before callback
                if self._stop_repeat:
                    break
                self.callback()
        else:
            time.sleep(self.duration)
            self.logger.info(f"Hit callback for {self.__repr__()}")
            self.callback()

        
    def start(self):
        self.logger.info(f"Starting timer for {self.duration} seconds")
        self.thread.start()

    def stop(self):
        self._stop_repeat = True


        