import sys
import time
import threading

class LoadingIndicator:
    def __init__(self):
        self.message = "Thinking"
        self.stop_flag = False
        self.thread = threading.Thread(target=self._animate, daemon=True)
        
        print("\033[92mLoading indicator initialized successfully\033[0m")

    def _animate(self):
        chars = ["|", "/", "-", "\\"]
        i = 0
        while not self.stop_flag:
            sys.stdout.write(f"\r{self.message} {chars[i % len(chars)]}")
            sys.stdout.flush()
            i += 1
            time.sleep(0.1)

    def start(self):
        self.stop_flag = False
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._animate, daemon=True)
            self.thread.start()

    def stop(self):
        self.stop_flag = True
        if self.thread and self.thread.is_alive():
            self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 3) + "\r")
        sys.stdout.flush()
        self.thread = None 