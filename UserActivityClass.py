import random


class userActivity:
    def __init__(self, window):
        self.noteMidiList = ["C0",
                             "C#0",
                             "D0",
                             "D#0",
                             "E0",
                             "F0",
                             "F#0",
                             "G0",
                             "G#0",
                             "A0",
                             "A#0",
                             "B0",
                             "C1",
                             "C#1",
                             "D1",
                             "D#1",
                             "E1",
                             "F1",
                             "F#1",
                             "G1",
                             "G#1",
                             "A1",
                             "A#1",
                             "B1",
                             "C2"
                             ]
        self.window = window
        self.strRandInt = ''
        self.randInt = self.generateWord()
        self.cur = 0
        self.accuracyDict = {"correct": 0, "incorrect": 0}


    def generateWord(self):
        randInt = []
        #StrRandInt might be usless, double check
        self.strRandInt = ''
        for i in range(0, 9):
            temp = random.randint(0, 24)
            randInt.append(temp)
            self.strRandInt = self.strRandInt + ' ' + self.noteMidiList[temp]
        self.window.setLabel(str(self.strRandInt))
        return randInt

    def on_press(self, key):
        #called from thread on mainPageClass.py
        print(key)
        #stores key presses for accuracys
        if key == self.randInt[0]:
            print("correct")
            self.accuracyDict["correct"] = (self.accuracyDict.get("correct") + 1)

            self.cur = self.cur + 1
            #if note is a #, remote xtra char. if not dont
            if self.noteMidiList[key][1] == '#':
                self.window.setLabel(self.strRandInt[4:])
                self.strRandInt = self.strRandInt[4:]
            else:
                self.window.setLabel(self.strRandInt[3:])
                self.strRandInt = self.strRandInt[3:]

            self.randInt.pop(0)
        else:
            print("Misinput")
            self.accuracyDict["incorrect"] = (self.accuracyDict.get("incorrect") + 1)
            self.window.setLabel(self.strRandInt)

        if len(self.randInt) == 0:
            self.randInt = self.generateWord()

        self.calcAccuracy()

    def calcAccuracy(self):
        #calculates accuracy in real time/on every key press.
        correct = self.accuracyDict.get("correct")
        incorrect = self.accuracyDict.get("incorrect")
        total_strokes = correct + incorrect
        accuracy = (correct / total_strokes) * 100
        print(accuracy)
        self.window.setAccuracyLabel(str(accuracy) + "% accuracy")
