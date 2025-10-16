import hid
import math
import time

# local library's
import utils

def main():
    devices = utils.list_devices()
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

    dev = utils.open_device_by_index(devices, idx)
    print("Device opened. Manufacturer:", dev.get_manufacturer_string(), "Product:", dev.get_product_string())

    print("Starting rainbow LED effect. Press Ctrl+C to stop.")
    try:
        i = 0
        while True:
            r, g, b = utils.rainbow_color(i)
            utils.send_led_report(dev, r, g, b)
            time.sleep(0.01)
            i += 1
    except KeyboardInterrupt:
        print("\nStopping rainbow effect...")
        dev.close()

if __name__ == "__main__":
    main()
