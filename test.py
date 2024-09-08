"""
Author: William C. Canin
Description: List file from a given directory, print and show the process in a Progressbar. Using Thread.
"""

from concurrent.futures import ThreadPoolExecutor
from tkinter import Tk, Button, W, messagebox
from tkinter.ttk import Progressbar
from threading import Thread
from os import walk
from os.path import join
# from time import sleep


class Engine(Thread):
    def __init__(self, path):
        Thread.__init__(self)
        self.path = path
        self.read_porcentege = 0

    def generator_files(self):
        for r, d, f in walk(self.path):
            for file in f:
                yield join(r, file)

    @staticmethod
    def process(filepath):
        print(filepath)

    def run(self):
        with ThreadPoolExecutor() as e:
            for file in self.generator_files():
                e.submit(self.process, file)
                self.read_porcentege += 100 / len(set(self.generator_files()))


class Window(Tk, Engine):
    def __init__(self, path):
        self.path = path
        Tk.__init__(self)
        Engine.__init__(self, self.path)

        self.title("Progressbar TKinter")
        self.geometry("240x100")
        self.resizable(False, False)
        self.configure(background="#d4d4d4")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.progressbar = Progressbar(self)
        self.progressbar.configure(length=235)
        self.progressbar.grid(column=0, row=0, sticky=W, padx=5, pady=5)
        self.btn1 = Button(self)
        self.btn1.configure(text="Start", cursor="hand2", background="#d4d4d4", foreground="#000")
        self.btn1.grid(column=0, row=1, sticky=W, padx=100, pady=5)
        self.btn1.configure(command=self.handle_start)

    def handle_start(self):
        self.start()
        self.btn1.configure(state="disabled")

        def update_progressbar():
            if self.is_alive():
                self.progressbar.config(value=self.read_porcentege)
                self.after(10, update_progressbar)
            else:
                self.progressbar.config(value=100)
                total = len(set(self.generator_files()))
                messagebox.showinfo("Progress", f"Done! {total} read files.")

        update_progressbar()


if __name__ == "__main__":
    w = Window("c:\\")
    w.mainloop()