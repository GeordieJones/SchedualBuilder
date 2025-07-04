import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem)

colors =   [('Red', '#FF0000'),
            ('Green', '#00FF00'),
            ('Blue', '#0000FF'),
            ('Black', '#000000'),
            ('Electric Green', '#41CD52'),
            ('Dark Blue', '#222840'),
            ('Yellow', '#F9E56d')]

def get_rgb(code):
    code_hex = code.replace('#', '')
    rgb = tuple(int(code_hex[i:i+2], 16) for i in (0,2,4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

app = QApplication()

table = QTableWidget()
table.setRowCount(len(colors))
table.setColumnCount(len(colors[0]) + 1)
table.setHorizontalHeaderLabels(['Name', 'Hex Code', 'Color'])

for i, (name,code) in enumerate(colors):
    item_name = QTableWidgetItem(name)
    item_code = QTableWidgetItem(code)
    item_color = QTableWidgetItem()
    item_color.setBackground(get_rgb(code))
    table.setItem(i, 0 , item_name)
    table.setItem(i, 1 , item_code)
    table.setItem(i, 2 , item_color)

table.show()
sys.exit(app.exec())