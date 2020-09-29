#!/usr/bin/env python3

import sys
import os
import subprocess
import time
import argparse
import tkinter as tk
from tkinter import ttk
from tkinter import *


parser = argparse.ArgumentParser(description='Check ms/ping for a specific url. Get feedback in diffrent colors, depends of ms and setpoint.\nDefault setpoint is 32ms')
parser.add_argument('-u', '--url', type=str, metavar='', required=True, help='Check ping for this website/url')
parser.add_argument('-s', '--set', type=int, metavar='', default=32, help='Setpoint above => bad ping')
parser.add_argument('-i', '--interval', type=int, metavar='', default=30, help='Set time interval in seconds; by default its 30 seconds')
parser.add_argument('-a', '--alert', action='store_true', help='message alert pop-up if connection failure')
args = parser.parse_args()


#alert argument window // root called except subprocess.CalledProcessError if args.alert
root = tk.Tk()

root.title("Cping")
root.geometry("250x55")
root.resizable(False, False)

message_label = Label(root, text="Disconnect: " + args.url)
message_label.pack(side=TOP, fill="x")

exit_button = ttk.Button(root, text="close", command=root.destroy)
exit_button.pack(side=BOTTOM, fill="x")




class output_color:
    GOOD = '\033[92m'    #green
    BAD = '\033[93m'     #yellow/orange
    FAIL = '\033[91m'    #red



def check_ping(url, pingSetPoint, interval):
    try:
        while True:
            terminal = ['ping', '-c 1', url]
            raw_feedback = subprocess.check_output(terminal).decode()
            feedback = raw_feedback.split()
            get_ping = feedback[13].split('=')[1]
            ping_float = float(get_ping)
            if ping_float >= pingSetPoint:
                print(output_color.BAD,"Bad connection", ping_float, "ms")
            else:
                print(output_color.GOOD,"Good connection", ping_float, "ms")

            time.sleep(interval)
            check_ping(args.url, args.set, args.interval)

    except subprocess.CalledProcessError:                    #no valid url
        print(output_color.FAIL, "CONNECTION FAILED: DISCONNECT OR NO VALID ADRESS")
        if args.alert == True:
            root.mainloop()




if __name__ == '__main__':
    try:
        check_ping(args.url, args.set, args.interval)

    except KeyboardInterrupt:                               #^C
        print(output_color.FAIL, ' Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
