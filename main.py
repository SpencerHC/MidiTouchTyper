from MainPageClass import *
from UserActivityClass import *


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


main()
