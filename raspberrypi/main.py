#!/usr/bin/env python3
# 2021 RaspiMote
# https://github.com/RaspiMote

from raspimote.pi import Pi
from sys import argv


def main(argv):
    if "-verbose" in argv or '-v' in argv:
        verbose = True
    else:
        verbose = False

    pi = Pi("192.168.1.16", "WiFi", verbose)

    """pi.add_buttons_configuration([
        {"pin": "21", "type_input": "button"},
        {"pin": "20", "type_input": "button"},
        {"pin": "16", "type_input": "button"},
        {"pin": "6", "type_input": "button"},
        {"pin": "13", "type_input": "button"},
        {"pin": "19", "type_input": "button"},
        {"pin": "26", "type_input": "button"},
    ])


    pi.add_ADC_Device_PCF8591(2)"""

    #pi.display_info(18, 23)

    #pi.add_USB_Device(0)
    pi.add_gamepad_device()
    pi.establish_connection()


if __name__ == '__main__':
    try:
        main(argv)
    except KeyboardInterrupt:
        print("Program ended")