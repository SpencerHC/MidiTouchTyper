import random
class userActivity:
    def __init__(self, window):
        self.window = window
        self.strRandInt = ''
        self.randInt = self.generateWord()
        self.cur = 0
        self.accuracyDict = {"correct": 0, "incorrect": 0}

    def generateWord(self):
        randInt = []
        self.strRandInt = ''
        for i in range(0, 9):
            temp = random.randint(32, 34)
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