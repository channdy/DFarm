import threading
import datetime
import time
import tkinter as tk
from queue import Queue

num_devices = 10
num_threads = 3


def deviceconnector(ip):
    # Simulate device connection by sleeping for 2 seconds
    time.sleep(2)
    print(f"done {ip} at {datetime.datetime.now()}\n")


def _queued_methods(queue: Queue) -> None:
    """Do queued tasks"""
    while not queue.empty():
        method, params = queue.get()
        # Execute the method "deviceconnector" with the provided parameters "ip=10.0.0.1"
        method(**params)
        queue.task_done()


def main() -> None:
    # Create a queue to store tasks
    queue: Queue = Queue()
    for i in range(num_devices):
        # Add device connection tasks to the queue
        queue.put((deviceconnector, {"ip": f"10.0.0.{i}"}))

    for idx in range(num_threads):
        # Create threads that execute queued tasks
        thread = threading.Thread(target=_queued_methods, args=(queue,))
        # Start the thread
        thread.start()
    # Wait for all tasks in the queue to be completed
    queue.join()


if __name__ == '__main__':
    root = tk.Tk()
    button_frame = tk.Frame(root)
    button_frame.pack(side="right")
    run_button = tk.Button(button_frame, text="Run HC", command=main)
    run_button.grid(padx=10, pady=10)
    root.mainloop()