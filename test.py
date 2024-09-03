import threading
import tkinter as tk
import time

must_stop = threading.Event()
counter_lock = threading.Lock()
counter = 0

def run_thread(root):
    global counter
    while not must_stop.is_set():
        time.sleep(1)
        with counter_lock:
            counter += 1
        if must_stop.is_set():
            return None
        root.event_generate('<<Counter>>', when="tail")


class CounterWindow(tk.Tk):
    # Window class for the counter
    def __init__(self):
        super().__init__()
        self.label = tk.Label(self, text="Hello!")
        self.label.pack()
        self.button = tk.Button(text="Start counter", command=self.start_thread)
        self.button.pack()
        self.bind("<<Counter>>", self.update_counter)
        
    def update_counter(self, event):
        #Writes counter to label, triggered by <<Counter>> event
        with counter_lock:
            self.label.configure(text=counter)
            
    def start_thread(self):
        #Button command to start the thread
        self.thread = threading.Thread(target=run_thread, args=(self, ))
        self.thread.start()
        self.button.configure(text="Stop counter", command=self.stop_thread)
        
    def stop_thread(self):
        must_stop.set()
        # self.thread.join() # Don't think it's nessasary
        self.button.configure(text="Exit counter", command=self.destroy)
        
# Start the app
window = CounterWindow()
window.mainloop()