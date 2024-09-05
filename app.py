import customtkinter
import tkinter
import tkinter.messagebox
import os
import time
from PIL import Image
import random
from CTkTable import *
from CTkXYFrame import *
import sqlite3
from ldplayer import LDPlayer
from database import DeviceDB, AccountDB, PageDB, Setting
# from tkfilebrowser import askopendirname, askopenfilenames, asksaveasfilename
from tkinter.filedialog import askopenfile

conn = sqlite3.connect("database.db")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DFarm Tool")
        self.geometry("1600x700")

        self.device_row_nums = []
        self.device_deleted_values = []

        self.acct_row_nums = []
        self.acct_deleted_values = []

        self.db_device = DeviceDB()
        self.db_device.create_table()
        self.db_device.delete_record()

        self.db_acct = AccountDB()
        self.db_acct.create_table()
        # self.db_acct.delete_record()

        self.db_setting = Setting()
        self.db_setting.create_table()

        self.acct_table = None

        # self.ldPlayer_dir = "D:\LDPlayer-Mod"
        self.ld_path_entry_text = customtkinter.StringVar()
        self.ldPlayer_dir = self.db_setting.get_setting("ldPlayer_dir")
        # print(self.ldPlayer_dir)
        if self.ldPlayer_dir is not None:
            self.ld_path_entry_text.set(self.ldPlayer_dir[0])
        else:
            self.ldPlayer_dir = ""

        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  DFarm", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Device",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Post",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Engagement",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.scrollable_frame = customtkinter.CTkScrollableFrame(self.home_frame, label_text="CTkScrollableFrame", width=200, height=200)
        # self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.scrollable_frame.grid_columnconfigure(0, weight=2)

        # Start Device Frame
        self.device_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=2)
        self.device_frame.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
        # self.device_frame.grid_rowconfigure(2, weight=1)

        self.device_table_frame = customtkinter.CTkFrame(self.device_frame, fg_color="transparent", width=100)
        self.device_table_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="nsew")

        self.device_ld_path_entry = customtkinter.CTkEntry(master=self.device_frame, placeholder_text="LD Path", width=300, textvariable=self.ld_path_entry_text)
        self.device_ld_path_entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.device_ld_path_entry.bind("<FocusOut>", self.ld_path_entry_focus_out)
        # self.device_ld_path_entry.bind("<FocusOut>", self.set_ld_path("Test"))
        # self.device_ld_path_entry.bind("<FocusIn>", self.entry_focus_in)
        # self.device_ld_path_entry.bind("<FocusOut>", self.entry_focus_out)
        # App.update()
        # self.device_ld_path_entry.focus_set()
        self.device_reload_btn = customtkinter.CTkButton(self.device_frame, text="Reload", width=70, command=self.reload_device)
        self.device_reload_btn.grid(row=0, column=1, padx=5, pady=0)
        self.device_kill_adb_btn = customtkinter.CTkButton(self.device_frame, text="Kill ADB", width=70)
        self.device_kill_adb_btn.grid(row=0, column=2, padx=5, pady=0)
        
        if self.ldPlayer_dir is not None:
            if os.path.isdir(self.ldPlayer_dir[0]):
                self.players = LDPlayer(self.ldPlayer_dir[0])
                self.db_device.update_device(self.players)
                # for key, value in self.players.list_ldplayer().items():
                #     # print(value)
                #     self.db.insert_data((int(key), value["name"], value["status"], value["serial"]))

        self.reload_device()

        #Start Account Frame
        self.account_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=2)
        self.account_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.account_check_status_btn = customtkinter.CTkButton(self.account_frame, text="Check Account", command=self.check_account)
        self.account_check_status_btn.grid(row=0, column=0, padx=(12, 0), pady=12)
        self.account_delete_btn = customtkinter.CTkButton(self.account_frame, text="Delete")
        self.account_delete_btn.grid(row=0, column=1, padx=0, pady=0)
        self.account_import_btn = customtkinter.CTkButton(self.account_frame, text="Import", command=self.open_import_file)
        self.account_import_btn.grid(row=0, column=2, padx=20, pady=(10, 10))
        self.account_table_frame = CTkXYFrame(self.account_frame, width=900)
        self.account_table_frame.grid(row=1, column=0, columnspan=10, padx=0, pady=0, sticky="nsew")
        

        self.build_acct_table()


        # self.import_account_frame = customtkinter.CTkFrame(self.home_frame)
        # self.import_account_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.account_list_frame = customtkinter.CTkFrame(self.home_frame)
        # self.account_list_frame.grid(row=1, column=0, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")


        # self.xy_frame = CTkXYFrame(self.home_frame)
        # self.xy_frame.grid(row=1, column=0, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # ld = LDPlayer("F:\LD-New")
        # ldplayers = ld.list_ldplayer()
        # # print(ldplayers)
        # for key, value in ldplayers.items():
        #     self.db.insert_data((int(key), value["name"], value["port"]))

        # devices = self.db.select_all()
        # device_tbl_val = [
        #     ["ID","Name","Port"]
        # ]
        # for device in devices:
        #     device_tbl_val.append(device)

        # # self.device_table = CTkTable(master=self.device_list_frame, values=device_tbl_val, hover=True, command=self.deviceTableCell, header_color="#2A8C55", hover_color="#B4B4B4", corner_radius=0)
        # self.device_table = CTkTable(master=self.device_list_frame, values=device_tbl_val, command=self.deviceTableCell, corner_radius=1)

        # for i in range(len(devices)):
        #     self.device_table.edit_row(i, hover_color='#a5b0af')

        # # self.device_table.configure(fg_color="#a5b0af", hover_color="#a5b0af")
        # self.device_table.edit_row(0, fg_color=("#4081BF","#212529"), font=("Roboto", 12, "bold"))
        # self.device_table.pack(expand=True, fill="both", padx=20, pady=20)

        # self.device_reload_btn = customtkinter.CTkButton(self.import_account_frame, text="Reload")
        # self.device_reload_btn.grid(row=0, column=0, padx=20, pady=(10, 10))
        # self.account_import_btn = customtkinter.CTkButton(self.import_account_frame, text="Import", command=self.open_FileDialog)
        # self.account_import_btn.grid(row=1, column=0, padx=20, pady=(10, 10))
        # self.account_start_btn = customtkinter.CTkButton(self.import_account_frame, text="Start", command=self.open_FileDialog)
        # self.account_start_btn.grid(row=1, column=1, padx=20, pady=(10, 10))

        # self.make_table_acct()

        # # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # # select default frame
        self.select_frame_by_name("home")

    def reload_device(self):
        self.devices_list = self.db_device.select_all()
        device_table_data = [
            ["ID", "LD Name", "Status", "Serial", "App", "IP Location"]
        ]
        for device in self.devices_list:
            device_table_data.append(device)
            
        self.device_table = CTkTable(master=self.device_table_frame, values=device_table_data, command=self.deviceTableCell, corner_radius=1, width=100)
        for i in range(len(self.devices_list)):
            self.device_table.edit_row(i, hover_color='#a5b0af')
        self.device_table.edit_row(0, fg_color=("#4081BF","#212529"), font=("Roboto", 12, "bold"))
        self.device_table.edit_column(0, width=15)
        self.device_table.pack(expand=True, fill="both", padx=0, pady=0)

    def check_account(self):
        for device in self.devices_list:
            print(f"start ldplayer id {device[0]}")
            self.players.start(device[0])
            time.sleep(5)

    def open_import_file(self):
        file = askopenfile(mode ='r', filetypes =[('Text Files', '*.txt')])
        if file is not None:
            # print(file)
            f = open(file, 'r')
            Lines = f.readlines()
            for line in Lines:
                self.db_acct.insert_data(line.strip().split("|"))
            self.acct_table.destroy()
            self.build_acct_table()

            # content = file.read()
            # print(content)

    def ld_path_entry_focus_out(self,event):
        self.db_setting.insert_data(("ldPlayer_dir", self.device_ld_path_entry.get()))
        # print("add element:", self.device_ld_path_entry.get())

    def set_ld_path(self, ld_path):
        print("LD Path")
        self.db_setting.insert_data(("ld_dir", ld_path))


    def build_acct_table(self):
        #id INTEGER  primary key, status text, device int, acct_name text, acct_uid text, page_name text, pass text, _2fa text, _token text, cookie text, app_pkg text, location text, store text
        acct_tbl_val = [
            ['ID', 'Status', 'Device Name', 'Account Name', 'UID', 'Page Name', 'Page ID', 'Password', '2FA', 'Token', 'Cookie', 'Package', 'Location', 'Store', 'Progress']
        ]
        self.accounts = self.db_acct.select_all()
        for account in self.accounts:
            # print(account)
            acct_tbl_val.append(account)
        self.acct_table = CTkTable(master=self.account_table_frame, values=acct_tbl_val, corner_radius=1, command=self.accountTableCell)
        
        self.acct_table.edit_row(0, fg_color=("#4081BF","#212529"), font=("Roboto", 12, "bold"))
        self.acct_table.edit_column(0, width=15)
        self.acct_table.edit_column(1, width=30)
        self.acct_table.edit_column(2, width=30)
        self.acct_table.edit_column(3, width=30)
        self.acct_table.pack(expand=True, fill="both", padx=0, pady=0)

    def accountTableCell(self, cell):
        if cell["row"]==0:
            return # don't change header
        if cell["row"] not in self.acct_row_nums:
            self.acct_table.select_row(cell["row"])
            self.acct_table.edit_row(cell["row"], fg_color=('#90EE90','#40445A'))
            self.acct_row_nums.append(cell["row"])
            self.acct_deleted_values.append(self.acct_table.get_row(cell["row"]))
        else:
            self.acct_table.deselect_row(cell["row"])
            self.acct_table.edit_row(cell["row"])
            self.acct_row_nums.remove(cell["row"])
            self.acct_deleted_values.remove(self.acct_table.get_row(cell["row"]))

    # def open_FileDialog(self):
    #     filepath = askopenfilenames(parent=self.account_frame, initialdir='/', initialfile='tmp', filetypes=[("Text", "*.txt"), ("All files", "*")])
    #     if filepath:
    #         f = open(filepath[0], 'r')
    #         Lines = f.readlines()
    #         for line in Lines:
    #             self.db_acct.insert_data(line.strip().split("|"))
    #         self.acct_table.destroy()
    #         self.build_acct_table()
        

    def deviceTableCell(self,cell):
        if cell["row"]==0:
            return # don't change header
        if cell["row"] not in self.device_row_nums:
            self.device_table.select_row(cell["row"])
            self.device_table.edit_row(cell["row"], fg_color=('#90EE90','#40445A'))
            self.device_row_nums.append(cell["row"])
            self.device_deleted_values.append(self.device_table.get_row(cell["row"]))
        else:
            self.device_table.deselect_row(cell["row"])
            self.device_table.edit_row(cell["row"])
            self.device_row_nums.remove(cell["row"])
            self.device_deleted_values.remove(self.device_table.get_row(cell["row"]))
        # print(self.device_row_nums)


    def selectCell(self, cell):
        print("row:", cell["row"])
        print("column:", cell["column"])
        print("value:", cell["value"])

        row = cell["row"]
        column = cell["column"]

    def pick_entry(self, e): print("click", e)

    def search_event(self):
        print("Test")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()

