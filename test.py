import tkinter as tk
import time
import queue
import threading
def runloop(thread_queue=None):
    result = 0
    for i in range(1000):
        pass
        #Do something with result
        time.sleep(5)
    result = result + 1
    thread_queue.put(result)
class MainApp(tk.Tk):
    def __init__(self):
            ####### Do something ######
            super(MainApp,self).__init__()
            self.myframe = tk.Frame(self)
            self.myframe.grid(row=0, column=0, sticky='nswe')
            self.mylabel = tk.Label(self.
            myframe) # Element to be updated
            self.mylabel.config(text='No message')
            self.mylabel.grid(row=0, column=0)
            self.mybutton = tk.Button(
            self.myframe,
            text='Change message111',
            command=self.update_text)
            self.mybutton.grid(row=1, column=0)
    def update_text(self):
            self.mylabel.config(text='Running loop')
            self.thread_queue = queue.Queue()
            self.new_thread = threading.Thread(
            target=runloop,
            kwargs={'thread_queue':self.thread_queue})
            self.new_thread.start()
            self.after(100, self.listen_for_result)
    def listen_for_result(self):
            try:
                self.res = self.thread_queue.get(0)
                self.mylabel.config(text='Loop terminated')
            except queue.Empty:
                self.after(100, self.listen_for_result)
if __name__ == "__main__":
    main_app = MainApp()
    main_app.mainloop()