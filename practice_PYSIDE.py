# from my other file that runs the logic
from main import get_classes, convert_to_days, ask_day
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ['Hallo Welt', 'Hei maailma', 'Hola mundo', 'Привет мир']
        self.button = QtWidgets.QPushButton('CLick me!')
        self.text = QtWidgets.QLabel('Hello World', alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())