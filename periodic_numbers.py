import argparse
import random
import time
import re
import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path


class Settings:
    SETTINGS_PATH = Path("settings.ini")

    def __init__(self):
        self.setSettings()
        self.content = str()

    def setSettings(self):
        if not self.SETTINGS_PATH.exists():
            print("Cannot find the settings file. This file will be create")
            self.SETTINGS_PATH.touch()

        with open(self.SETTINGS_PATH, 'r', encoding="utf-8") as file:
            self.content = file.read()

        if not self.content:
            self.content = """
width: 800
height: 600
speed_view: 1000
nums_count: 100
"""
            print(f"Default content of {self.SETTINGS_PATH.absolute()} is:\n{self.content}")

            with open(self.SETTINGS_PATH, 'w', encoding="utf-8") as file:
                file.write(self.content)

    @staticmethod
    def getScreenSize() -> str:
        with open(Settings.SETTINGS_PATH, 'r', encoding="utf-8") as file:
            content = file.read()

        pattern_width = "width: (\\d*)"
        pattern_height = "height: (\\d*)"
        match_width = re.search(pattern_width, content)
        match_height = re.search(pattern_height, content)
        if not match_width or not match_height:
            print("Cannot match width or height in the settings. Set default value")
            return str("800x600")

        return f"{match_width.group(1)}x{match_height.group(1)}"

    @staticmethod
    def getTimeInterval() -> int:
        with open(Settings.SETTINGS_PATH, 'r', encoding="utf-8") as file:
            content = file.read()

        pattern = "speed_view: (\\d*)"
        match = re.search(pattern, content)
        if not match:
            print("Cannot match time interval for showing numbers. Set default value")
            return 1000

        return match.group(1)

    @staticmethod
    def setTimeInterval(new_interval: int):
        with open(Settings.SETTINGS_PATH, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        content = []
        for line in lines:
            if line.startswith("speed_view: "):
                line = line.replace(line.split(' ')[-1], str(new_interval) + '\n')
            content.append(line)

        with open(Settings.SETTINGS_PATH, 'w', encoding="utf-8") as file:
            file.write("".join(content))

    @staticmethod
    def getCount() -> int:
        with open(Settings.SETTINGS_PATH, 'r', encoding="utf-8") as file:
            content = file.read()

        pattern = "nums_count: (\\d*)"
        match = re.search(pattern, content)
        if not match:
            print("Cannot match counter for quantity of numbers. Set default value")
            return 100

        return match.group(1)


class NumberMemory:
    NUMBERS_xN = [ 46, 77, 81, 70, 118 ]

    def __init__(self, need_calibrate: bool):
        self.settings_ = Settings()
        self.need_calibrate = need_calibrate

        upgrade_max = sum(self.NUMBERS_xN[0:1])
        self.max_counter = (upgrade_max + 5) if self.need_calibrate else sum(self.NUMBERS_xN[0:5])
        self.counter = upgrade_max

        self.prepareWindow()

    def prepareWindow(self):
        self.root = tk.Tk()
        self.root.title("Periodic numbers")
        self.root.geometry(Settings.getScreenSize())

        self.ready_button = tk.Button(self.root, text="Ready", font=48, command=self.generateNumber)
        self.setButtonPlace()

        self.number_label = tk.Label(self.root, text="", font=48)

        self.root.mainloop()

    def enterNumber(self, curr_number: int):
        user_input = simpledialog.askstring("Enter the answer", "Enter number:")
        if user_input and not user_input.isdigit():
            messagebox.showwarning("FuckYou", "You need to type an integer value!")
            self.enterNumber(curr_number)

        is_number_correct = bool(curr_number == int(user_input))
        new_interval = int(Settings.getTimeInterval()) - 50 if is_number_correct \
                       else int(Settings.getTimeInterval()) + 20
        if self.need_calibrate:
            Settings.setTimeInterval(new_interval if new_interval >= 50 else 50)

        if is_number_correct:
            print("Fuck Yeah")

        # write the result into a file and calc statistics

        self.showButton()

    def generateNumber(self):
        self.hideButton()

        if self.counter >= self.max_counter:
            exit(0)

        curr_number = int(0)
        if self.counter < self.NUMBERS_xN[0]:
            curr_number = random.randint(10, 99)
        elif self.counter < sum(self.NUMBERS_xN[0:1]):
            curr_number = random.randint(100, 999)
        elif self.counter < sum(self.NUMBERS_xN[0:2]):
            curr_number = random.randint(1000, 9999)
        elif self.counter < sum(self.NUMBERS_xN[0:3]):
            curr_number = random.randint(10000, 99999)
        elif self.counter < sum(self.NUMBERS_xN[0:4]):
            curr_number = random.randint(100000, 999999)

        self.number_label.place(relx=0.5, rely=0.5, anchor="center")
        self.number_label.config(text=str(curr_number))
        self.root.update()

        self.root.after(Settings.getTimeInterval(), self.enterNumber, curr_number)
        self.root.after(Settings.getTimeInterval(), self.number_label.place_forget)

        self.counter += 1

    def setButtonPlace(self):
        self.ready_button.place(relx=0.5, rely=0.5, anchor="center")

    def hideButton(self):
        self.ready_button.config(state=tk.DISABLED)
        self.ready_button.place_forget()

    def showButton(self):
        self.setButtonPlace()
        self.ready_button.config(state=tk.ACTIVE)


def parseArgs():
    parser = argparse.ArgumentParser(description="Arguments parser")
    parser.add_argument("-c", "--calibrate", action="store_true",
                        help="Need calibrate time to show?")
    return parser.parse_args()


if __name__ == "__main__":
    args = parseArgs()
    NumberMemory(args.calibrate)
