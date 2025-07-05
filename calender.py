import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem)

weekdays = [('monday',['math', 'science']),('tuesday',['aero 121']),('wednesday',['calc 2']),('thursday',[]),('friday',[]),('saturday',[]),('sunday',[])]

app = QApplication([])

table = QTableWidget()
table.setRowCount(len(weekdays))
table.setColumnCount(3)
table.setHorizontalHeaderLabels(['Day', 'classes', 'study times'])

for i, (weekday, classes) in enumerate(weekdays):
    item_day = QTableWidgetItem(weekday)
    item_classes = QTableWidgetItem(', '.join(classes) if classes else "None")
    item_study = QTableWidgetItem('')
    table.setItem(i, 0 , item_day)
    table.setItem(i, 1 , item_classes)
    table.setItem(i, 2 , item_study)

table.resizeColumnsToContents()
table.setWindowTitle("Weekly Planner")
table.show()
sys.exit(app.exec())




