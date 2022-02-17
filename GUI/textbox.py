from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QLineEdit, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
#import pyqtgraph as pg
import sys
# from host import *

class Textbox_Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Hello I am text box'
        self.left, self.right = 0, 0  # Position relative to screen, (0,0) is top left corner
        self.width, self.height = 1000, 1000
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.right, self.width, self.height)

        # Creating the textbox widget
        self.textbox = QLineEdit(self)
        self.textbox.resize(int(self.width*0.8), 30)
        self.textbox.move(self.width-(self.width- 20), self.height-50)
        self.textbox.returnPressed.connect(self.on_enter)

        # Creating a text label to return what happened from last command
        self.label = QLabel(self)
        font = self.label.font()
        #self.label.setPointSize(30)
        self.label.resize(int(self.width*0.8), 30)
        self.label.setFont(font)
        self.label.move(self.width-(self.width- 20), self.height-100)
        self.label.setText('Yo')

        # Can make graph?


        # Creating the button in the window
        self.button = QPushButton('I am text hello', self)
        self.button.move(20, 80)

        # Connecting the button widget we made to click interaction
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_enter(self):
        textboxValue = self.textbox.text()
        self.textbox.setText('')
        print('The string returned is: ' + textboxValue)
        #send_command(textboxValue)  # Using Aidan's zmq
        if textboxValue == 'command':
            self.label.setText("The input command '{}' was correct, and executed.".format(textboxValue))
        else:
            self.label.setText("The input command '{}' is not a real command, please retry.".format(textboxValue))
        # if command sent != viable command, then prompt for a new
        # return textboxValue

    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    textwindow = Textbox_Window()
    sys.exit(app.exec_())
