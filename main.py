# This is a sample Python script.
import sys
import random
import pygame
from pygame import midi
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
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
        self.label = ""
        self.accuracy = ""
        self.widget()

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        ## use above line or below
        self.resize(self.width, self.height)
        self.move(self.left, self.top)

        # add label
        self.label1 = QLabel(self, text=self.label)
        self.label1.setFont(QFont('Arial', 20))
        # margin: left, top; width, height
        self.label1.setGeometry(QRect(50, 5, 400, 50))
        self.label1.setWordWrap(True)  # allow word-wrap

        self.accuracyLabel = QLabel(self, text=self.accuracy)
        # margin: left, top; width, height
        self.accuracyLabel.setGeometry(QRect(50, 30, 200, 50))
        self.accuracyLabel.setWordWrap(True)
        self.show()

    def setLabel(self, labelVal):
        self.label1.setText(labelVal)
        self.label = labelVal

    def setAccuracyLabel(self, accuracyVal):
        self.accuracyLabel.setText(accuracyVal)
        self.accuracy = accuracyVal


class myThread(QThread):
    def __init__(self, mainActivity):
        self.myActivity = mainActivity
        super().__init__()

    def run(self):
        pygame.init()
        pygame.fastevent.init()
        midi.init()
        event_get = pygame.fastevent.get
        event_post = pygame.fastevent.post
        i = midi.Input(midi.get_default_input_id())
        while True:
            if i.poll():
                event = i.read(1)
                if event[0][0][0] == 150:
                    self.myActivity.on_press(event[0][0][1])


def main():
    app = QApplication(sys.argv)
    w = MainPage(title="PyQt5")
    mainActivity = userActivity(w)
    thread = myThread(mainActivity)
    thread.finished.connect(app.exit)
    thread.start()

    # listener = Listener(on_press=myActivity.on_press)
    # listener.start()

    sys.exit(app.exec_())


class userActivity:
    def __init__(self, window):
        self.window = window
        #self.MainWindow = window
        self.strRandInt = ''
        self.randInt = self.generateWord()
        self.cur = 0
        self.accuracyDict = {"correct": 0, "incorrect": 0}

    def generateWord(self):
        randInt = []
        self.strRandInt = ''
        for i in range(0, 9):
            temp = random.randint(36, 38)
            randInt.append(temp)
            self.strRandInt = self.strRandInt + ' ' + str(temp)
        self.window.setLabel(str(self.strRandInt))
        return randInt

    def on_press(self, key):
        if key == self.randInt[0]:
            print("correct")
            self.accuracyDict["correct"] = (self.accuracyDict.get("correct") + 1)

            self.cur = self.cur + 1
            self.window.setLabel(self.strRandInt[3:])
            self.strRandInt = self.strRandInt[3:]
            self.randInt.pop(0)
        else:
            print("Misinput")
            self.accuracyDict["incorrect"] = (self.accuracyDict.get("incorrect") + 1)

        if len(self.randInt) == 0:
            self.calcAccuracy()
            self.randInt = self.generateWord()
        self.calcAccuracy()

    def calcAccuracy(self):
        correct = self.accuracyDict.get("correct")
        incorrect = self.accuracyDict.get("incorrect")
        total_strokes = correct + incorrect
        accuracy = (correct / total_strokes) * 100
        print(accuracy)
        self.window.setAccuracyLabel(str(accuracy) + "% accuracy")


main()
