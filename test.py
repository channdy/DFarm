import tkinter as tk
import tkinter.ttk as ttk
 
 
class MainFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process = tk.IntVar(value=5)
        self.after_id = None
 
        self.progressbar = ttk.Progressbar(
            self.master, length=200, maximum=10, variable=self.process
        )
        self.progressbar.grid(row=1)
 
        self.add_button = ttk.Button(
            self.master, text="Water +", command=self.add_water
        )
        self.sub_button = ttk.Button(
            self.master, text="Water -", command=self.sub_water
        )
 
        self.label = ttk.Label(self.master, textvariable=self.process)
 
        self.label.grid(row=0)
        self.add_button.grid(row=0, sticky="e")
        self.sub_button.grid(row=0, sticky="w")
 
    def reset_water(self):
        self.process.set(5)
        self.after_id = None
 
    def reset_after(self, delay_ms):
        if self.after_id:
            self.after_cancel(self.after_id)
 
        self.after_id = self.after(delay_ms, self.reset_water)
 
    def add_water(self):
        progress_value = self.process.get()
        if progress_value < self.progressbar["maximum"]:
            self.process.set(progress_value + 1)
            self.reset_after(60000)
 
    def sub_water(self):
        progress_value = self.process.get()
        if progress_value > 0:
            self.process.set(progress_value - 1)
            self.reset_after(60000)
 
 
if __name__ == "__main__":
    tk_app = tk.Tk()
    main_frame = MainFrame()
    tk_app.mainloop()