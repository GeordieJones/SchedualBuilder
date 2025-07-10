import core.optimizer as optimizer
import core.helpper_files as hf
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem)


def show_data(class_days, vals):
    optimizer.optimize(class_days, vals)
    for day in class_days:
        print(f"{day.name} has {len(day.study_times)} study sessions.")

    #app = QApplication([])
    table = QTableWidget()
    table.setRowCount(len(class_days))
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(['Day', 'Schedule', 'Classes', 'Activities','Study Times'])

    day_name_map = {
        'm': 'Monday',
        't': 'Tuesday',
        'w': 'Wednesday',
        'th': 'Thursday',
        'f': 'Friday',
        'sat': 'Saturday',
        'sun': 'Sunday'
    }
    for i, day in enumerate(class_days):
        full_day_name = day_name_map.get(day.name, day.name)
        item_day = QTableWidgetItem(full_day_name)


        if not day.courses:
            classes_str = 'No classes'
        else:
            classes_str = '\n'.join(f' {c.name} ({c.time_range()})' for c in day.courses)


        # Build study times string
        if not day.study_times:
            study_str = 'No study sessions'
        else:
            study_str = '\n'.join(f'{s.name} ({s.time_range()})' for s in day.study_times)



        if not day.activities:
            activity_str = 'No activities'
        else:
            activity_str = '\n'.join(f'{a.name} ({a.time_range()})' for a in day.activities)


            #before was activity_str = '\n'.join(day.study_times)


        # Build combined schedule string

        combined_list = hf.get_all_sorted_items(day)
        if not combined_list:
            combined_list = ['No classes, activities, or study sessions']
        


        item_schedule = QTableWidgetItem('\n'.join(combined_list))
        item_schedule.setTextAlignment(Qt.AlignTop)
        item_schedule.setFlags(item_schedule.flags() | Qt.ItemIsEditable)

        item_classes = QTableWidgetItem(classes_str)
        item_classes.setTextAlignment(Qt.AlignTop)
        item_classes.setFlags(item_classes.flags() | Qt.ItemIsEditable)

        item_activity = QTableWidgetItem(activity_str)
        item_activity.setTextAlignment(Qt.AlignTop)
        item_activity.setFlags(item_activity.flags() | Qt.ItemIsEditable)

        item_study = QTableWidgetItem(study_str)
        item_study.setTextAlignment(Qt.AlignTop)
        item_study.setFlags(item_study.flags() | Qt.ItemIsEditable)

        table.setItem(i, 0, item_day)
        table.setItem(i, 1, item_schedule)
        table.setItem(i, 2, item_classes)
        table.setItem(i, 3, item_activity)
        table.setItem(i, 4, item_study)
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.setWordWrap(True)
    table.resize(800, 600)
    for row in range(table.rowCount()):
        if table.rowHeight(row) < 50:
            table.setRowHeight(row, 50)
    table.setWindowTitle('Weekly Class Schedule')
    table.show()
    return table