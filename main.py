import hid
import math
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading as th
from colorama import Fore, Style

# local library's
import ds4utils
import utils

# adding const
INVIS_COL = "#000001"

# other variables
currentdevice = None
bg_col = "#000122"

# functions for bind events
def on_select_choose_device(event):
    cb = event.widget
    
    devices = hid.enumerate()
    for _, device in enumerate(devices):
        product = device.get("product_string") or "N/A"
        manufacturer = device.get("manufacturer_string") or "N/A"
        _this = f"{manufacturer} - {product}"
        
        if cb.get() == _this:
            path = device.get("path")
            if isinstance(path, str):
                path.encode()
            
            currentdevice = hid.device()
            currentdevice.open_path(path)
            messagebox.showinfo("-- DS4MENU", "Connected to: %s" % (_this))
            return
    
    messagebox.showerror("--DS4MENU", "Couldnt connect to %s" % (_this))
        
    cb.selection_clear()
    cb.icursor(tk.END)
    cb.master.focus_set()
    
    

class Ds4:
    def __init__(self):
        """Initialize Ds4 class"""
        self.root = tk.Tk()
        
        self.root.resizable(False, False)
        self.root.geometry("760x386")
        self.root.title("DS4MENU |⭐")
        self.root.config(bg=bg_col)
        self.root.wm_attributes("-transparentcolor", INVIS_COL)
        
        self.main_gui_th = th.Thread(
            target = self.main_gui
        ); self.main_gui_th.daemon = True
    
    def run_gui(self):
        """Run function from Ds4 class."""
        # setup WM_FUNC
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)

        # everything else lol
        self.main_gui_th.start()
        self.root.mainloop()
    
    def main_gui(self):
        """GUI Function that handles **most** interface features"""
        self.lbl_choose_device = tk.Label(
            self.root,
            font=utils.FNT_FUTURA.c14,
            bg=bg_col,
            text="Choose Controller",
            fg="#FFFFFF"
        ); self.lbl_choose_device.place(
            x=15, y=15, width=180, height=90
        )
        
        self.drop_choose_device = ttk.Combobox(
            self.root,
            values= ["Hello", "Twin"]
        ); self.drop_choose_device.place(
            x=200, y=45, width=170, height=30
        ); self.drop_choose_device.config(
            font=utils.FNT_FUTURA.c12
        )
        
        self.drop_choose_device.state(["readonly"])
        self.drop_choose_device.set("Select a Controller.")
        self.drop_choose_device.bind("<<ComboboxSelected>>", on_select_choose_device)
        
        def tkafter_drop_choose_device() -> None:
            values = []; devices = hid.enumerate()
            for _, device in enumerate(devices):
                product = device.get("product_string") or "N/A"
                manufacturer = device.get("manufacturer_string") or "N/A"
                values.append(f'{manufacturer} - {product}')
            
            self.drop_choose_device.config(values=values)
            self.root.after(10, tkafter_drop_choose_device)
        self.root.after(10, tkafter_drop_choose_device)
        
        self.lbl_choose_rgb = tk.Label(
            self.root,
            font=utils.FNT_FUTURA.c14,
            bg=bg_col,
            text="RGB Values",
            fg="#FFFFFF"
        ); self.lbl_choose_rgb.place(
            x=15, y=85, width=180, height=40
        )
        
        self.spin_rgb_r = tk.Spinbox(
            self.root, from_=0, to=255, bg="#FF0000", font=utils.FNT_FUTURA.c12
        ); self.spin_rgb_r.place(x=200, y=85, width=40, height=40)
        
        self.spin_rgb_g = tk.Spinbox(
            self.root, from_=0, to=255, bg="#00FF00", font=utils.FNT_FUTURA.c12
        ); self.spin_rgb_g.place(x=240, y=85, width=40, height=40)
        
        self.spin_rgb_b = tk.Spinbox(
            self.root, from_=0, to=255, bg="#0000FF", font=utils.FNT_FUTURA.c12
        ); self.spin_rgb_b.place(x=280, y=85, width=40, height=40)

    def destroy(self, code=0):
        """completely stops everything"""
        self.root.destroy()
        exit(code=code)

def main() -> None:
    # add whatever here
    ds4 = Ds4()
    ds4.run_gui()
    
    # wait until user closes
    
    while 1: time.sleep(1) 

if __name__ == "__main__":
    main()
