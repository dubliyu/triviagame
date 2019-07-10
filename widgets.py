import random
import sys
import math
import os
from itertools import count

from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QListWidget, QLabel, QVBoxLayout, QTextEdit, QListWidgetItem, QHBoxLayout, QPushButton, QBoxLayout
from question import Question


class QuestionManagerWidget(QListWidget):           # - QWidget
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.HEIGHT = 500
        self.WIDTH = 300

        self.setFrameShape(self.NoFrame)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)


        self._allow_height_change = False
        self._child_widgets = []
        self.qid_list = Question.get_question_ids()


    def add_question_widget(self, question):
        #load question


        #set up list item
        item = QListWidgetItem()

        # Create widgets
        widget = QWidget()
        widget.setAutoFillBackground(True)
        product_name = QLabel()
        product_name.setText(question.getName())

        pal = QPalette()
        pal.setColor(QPalette.Background, QtCore.Qt.darkGray)
        widget.setPalette(pal)


        #image
        pixmap = QPixmap(question.getImagePath())
        product_image = QLabel()
        product_image.setFixedSize(self.WIDTH, self.HEIGHT/1.5)
        product_image.setPixmap(pixmap.scaled(product_image.size(), QtCore.Qt.KeepAspectRatio))
        product_image.setAlignment(QtCore.Qt.AlignCenter)
        product_image.setAutoFillBackground(False)


        #buttons
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")
        buttons = [edit_button, delete_button]

        #add widgets to layout
        widgetLayout = QVBoxLayout()
        widgetLayout.addWidget(product_image)
        widgetLayout.addWidget(product_name)
        widgetLayout.addWidget(edit_button)
        widgetLayout.addWidget(delete_button)
        # widgetLayout.addStretch()
        # widgetLayout.setAlignment(QtCore.Qt.AlignCenter)

        #add widget to QListView
        widget.setLayout(widgetLayout)
        widget.setFixedSize(self.WIDTH, self.HEIGHT)
        widget.setParent(self)
        self._child_widgets.append(widget)



        self._move_panels()
        return buttons

    def _move_panels(self):
        num_per_row = max(int((self.width()) / self.WIDTH), 1)

        for i in range(len(self._child_widgets)):
            y = int(i / num_per_row)
            x = i % num_per_row
            self._child_widgets[i].move(x * self.WIDTH, y * self.HEIGHT)

        num_rows = math.ceil(len(self._child_widgets) / float(num_per_row))
        min_height = num_rows * self.HEIGHT
        self.setFixedHeight(min_height)


    def resizeEvent(self, QResizeEvent):
        self._move_panels()

if __name__ == '__main__':
#    import callback_fix
    app = QApplication(sys.argv)
    gui = QuestionManagerWidget()
    gui.show()
    app.exec_()

