import sys
import random
import pygame
from pygame import midi
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication, QThread, Qt, QRunnable, QThreadPool, QObject, pyqtSignal


class MainPage(QWidget):
    def __init__(self, title=" "):
        super().__init__()  # inherit init of QWidget
        self.thread = QThread()
        self.title = title
        self.left = 1000
        self.top = 1000
        self.width = 800
        self.height = 600
        self.lesson_string = ""
        self.accuracy = ""
        self.calibrate_string = ""
        self.widget()

        self.calibrateClicked = False
        self.middle_c: int

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        ## use above line or below
        self.resize(self.width, self.height)
        self.move(self.left, self.top)

        # add label
        self.lesson_label = QLabel(self, text=self.lesson_string)
        self.lesson_label.setFont(QFont('Arial', 20))
        # margin: left, top; width, height
        self.lesson_label.setGeometry(QRect(50, 5, 800, 50))
        self.lesson_label.setWordWrap(True)  # allow word-wrap
    #Calibrate Button
        self.button = QPushButton("Calibrate", self)
        self.button.setToolTip('Calibrate by pressing middle C')
        self.button.move(550, 20)

    #Calibrate Label
        self.calibrate_label = QLabel(self, text=self.calibrate_string)
        self.calibrate_label.setFont(QFont('Arial', 10))
        # margin: left, top; width, height
        self.calibrate_label.setGeometry(QRect(550, 50, 50,50))
        self.calibrate_label.setWordWrap(True)

        self.button.clicked.connect(self.on_click)



        self.accuracyLabel = QLabel(self, text=self.accuracy)
        # margin: left, top; width, height
        self.accuracyLabel.setGeometry(QRect(50, 30, 200, 50))
        self.accuracyLabel.setWordWrap(True)

        self.show()

    @pyqtSlot()
    def on_click(self):
        self.button.setText("Calibrating...")
        self.calibrateClicked = True


    def setLabel(self, labelVal):
        self.lesson_label.setText(labelVal)
        self.lesson_string = labelVal

    def setAccuracyLabel(self, accuracyVal):
        self.accuracyLabel.setText(accuracyVal)
        self.accuracy = accuracyVal


class myThread(QThread):
    #Thread that drives midi input, essentially a midi listener
    def __init__(self, mainActivity):
        self.myActivity = mainActivity
        self.middleC = 0
        super().__init__()

    def run(self):

        pygame.init()
        pygame.fastevent.init()
        midi.init()
        event_get = pygame.fastevent.get
        event_post = pygame.fastevent.post
        i = midi.Input(midi.get_default_input_id())

        while True:
            #checks if calibrate button was click.
            #if yes, read as though it's calibration
            #otherwise, read as lesson note press
            calibrateClicked = self.myActivity.window.calibrateClicked
            if calibrateClicked and i.poll():
                event = i.read(1)
                if event[0][0][0] == 150:
                    self.middleC = event[0][0][1]
                    self.myActivity.window.calibrateClicked = False
                    self.myActivity.window.button.setText("Calibrated")

            elif i.poll() and not calibrateClicked:
                event = i.read(1)
                if event[0][0][0] == 150:
                    start = self.calibrationCalc()
                    self.myActivity.on_press(event[0][0][1] - start)

    def calibrationCalc(self):
        end = self.middleC + 12
        return self.middleC - 12
