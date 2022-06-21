import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTextBrowser, QCheckBox
from threading import Thread
import time
import win32api
import win32con

import keypress
import ImageRecognition


class Bot:
    def __init__(self):
        pass

    def move(self, direction):
        if direction == "right":
            keypress.press("d")

        if direction == "left":
            keypress.press("a")

        if direction == "jump":
            keypress.press("w")

    def attack(self, repeat):
        keypress.press("spacebar")

    def place_block(self, cords):
        pass


class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        uic.loadUi("mainWindow.ui", self)

        self.log = self.findChild(QTextBrowser, "log_tb")

        self.start_button = self.findChild(QPushButton, "startbot_pb")
        self.start_button.clicked.connect(self.start_t1)

        self.stop_button = self.findChild(QPushButton, "stopbot_pb")
        self.stop_button.clicked.connect(self.stop_t1)

        self.t1 = Thread(target=self.run_bot)

        self.status_t1 = False

        self.show()

    def start_t1(self):
        time.sleep(2)
        if self.t1.is_alive():
            pass
        else:
            self.status_t1 = True
            try:
                self.log.append(str("Connecting"))
                print("Connected")
                self.t1 = Thread(target=self.run_bot)
                self.t1.start()
            except Exception as e:
                self.log.append(f"Error: {str(e)}")
                print(f"Error: {str(e)}")

    def stop_t1(self):
        self.status_t1 = False
        self.log.append(str("Disconnected"))
        print("Disconnected")

    def start_bot(self):
        print("Starting bot")
        bot = Bot()
        self.run_bot()

    def run_bot(self):
        print("Bot running...")
        direction = "left"
        pressing = False
        changed_direction = False
        while self.status_t1:
            if not self.status_t1:
                break

            pixelvalue = ImageRecognition.check_pixel_below()
            pixelsum = pixelvalue[0] + pixelvalue[1] + pixelvalue[2]
            print(pixelsum)

            if direction == "left" and not pressing:
                keypress.pressAndHold("a")
                pressing = True

                win32api.SetCursorPos((1010, 540))
                time.sleep(0.05)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # Press mouse down

            if direction == "right" and not pressing:
                keypress.pressAndHold("d", "spacebar")
                pressing = True
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)  # Release mouse

            if pixelsum < 220 and not changed_direction:
                pressing = False
                changed_direction = True
                if direction == "left":
                    direction = "right"
                    keypress.release("a")

                else:
                    direction = "left"
                    keypress.release("d", "spacebar")

                time.sleep(0.5)

            if pixelsum > 320 and changed_direction:
                changed_direction = False

                pressing = False




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
    sys.exit()
