import hid
import math
import time
import tkinter as tk
import threading as th
from colorama import Fore, Style


# local library's
import utils

class Ds4:
    def __init__(self):
        """Initialize Ds4 class"""
        self.root = tk.Tk()
        
        self.root.resizable(False, False)
        self.root.geometry("760x386")
        self.root.title("DS4MENU |⭐")
        self.root.config(bg="#000122")
        
        self.main_gui_th = th.Thread(
            target = self.main_gui
        ); self.main_gui_th.daemon = True
    
    def run(self):
        """Run function from Ds4 class."""
        self.main_gui_th.start()
        self.root.mainloop()
    
    def main_gui(self):
        """GUI Function that handles **most** interface features"""
        self.lbl_choose_device = tk.Label(
            self.root
        ); self.lbl.place(x=25,y=25, width=60, height=20)
    
    def stop(self, code=0):
        """Exit?? (idfk its literally just exit() func)"""
        exit(code)

def main():
    # add whatever here
    ds4 = Ds4()
    ds4.run()
    
    # wait until user closes
    while 1: time.sleep(1) 

if __name__ == "__main__":
    main()
