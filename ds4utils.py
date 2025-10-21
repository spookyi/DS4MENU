import hid
import math
import time

def list_devices():
    """List all connected HID devices."""
    devices = hid.enumerate()
    print("Index  Vendor   Product   Path                                Manufacturer      Product")
    for i, d in enumerate(devices):
        vid = d['vendor_id']
        pid = d['product_id']
        manu = d.get('manufacturer_string') or ""
        prod = d.get('product_string') or ""
        path = d.get('path')
        if isinstance(path, bytes):
            path = path.decode()
        print(f"{i:3d}    {vid:04x}   {pid:04x}   {path}   {manu:18.18}   {prod}")
        print(devices)
    return devices

def open_device_by_index(devices, idx):
    """Open HID device by index, ensuring path is bytes."""
    d = devices[idx]
    path = d.get('path')
    if isinstance(path, str):
        path = path.encode()
    device = hid.device()
    device.open_path(path)
    return device

def send_led_report(device, r, g, b, small_motor=0, large_motor=0, flash_on=0, flash_off=0):
    """
    Send a proper USB DS4 LED report (Report ID 0x05, 32 bytes total).
    """
    report = [
        0x05,        # Report ID
        0xFF,        # Enable flags
        small_motor, # Right motor
        large_motor, # Left motor
        0, 0,        # Nothing lol
        r, g, b,     # LED colors
        flash_on,    # Flash on
        flash_off,   # Flash off
    ] + [0x00] * (32 - 9)  # Pad 32 bytes
    
    try:
        device.write(bytearray(report))
    except Exception as e:
        print("Failed to send report:", e)



def rainbow_color(i):
    """
    Compute RGB values for a smooth rainbow effect using sine waves.
    """
    r = int(math.sin(i * 0.1 + 0) * 127 + 128)
    g = int(math.sin(i * 0.1 + 2) * 127 + 128)
    b = int(math.sin(i * 0.1 + 4) * 127 + 128)
    return r, g, b

def main():
    devices = list_devices()
    if not devices:
        print("No HID devices found.")
        return

    idx_input = input("Choose device index to open (or 'q' to quit): ").strip()
    if idx_input.lower() == 'q':
        return

    try:
        idx = int(idx_input)
    except ValueError:
        print("Invalid index")
        return
    if idx < 0 or idx >= len(devices):
        print("Index out of range")
        return

    dev = open_device_by_index(devices, idx)
    print("Device opened. Manufacturer:", dev.get_manufacturer_string(), "Product:", dev.get_product_string())

    print("Starting rainbow LED effect. Press Ctrl+C to stop.")
    try:
        i = 0
        while True:
            r, g, b = rainbow_color(i)
            send_led_report(dev, r, g, b)
            time.sleep(0.1)
            i += 1
    except KeyboardInterrupt:
        print("\nStopping rainbow effect...")
        dev.close()

if __name__ == "__main__":
    main()