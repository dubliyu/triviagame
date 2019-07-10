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

        self.HEIGHT = 400
        self.WIDTH = 300

        self.setFrameShape(self.NoFrame)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)


        self._allow_height_change = False
        self._child_widgets = []
        self.qid_list = Question.get_question_ids()
        self.add_question_widgets()


    def add_question_widgets(self):
        for i in self.qid_list:
            #load question
            question = Question.createQuestion(i)

            #set up list item
            item = QListWidgetItem()

            # Create widget
            widget = QWidget()
            product_name = QLabel(question.getName())
            pixmap = QPixmap(question.getImagePath())

            product_image = QLabel()
            product_image.setFixedSize(self.WIDTH/2, self.HEIGHT/2)
            product_image.setPixmap(pixmap.scaled(product_image.size(), QtCore.Qt.KeepAspectRatio))
            product_image.setAlignment(QtCore.Qt.AlignCenter)

            #buttons
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda: self.open_question(qid))
            delete_button = QPushButton("Delete")
            qid = question.getID()
            delete_button.clicked.connect(lambda: self.delete_question(qid))

            #add widgets to layout
            widgetLayout = QVBoxLayout()
            widgetLayout.addWidget(product_image)
            widgetLayout.addWidget(product_name)
            widgetLayout.addWidget(edit_button)
            widgetLayout.addWidget(delete_button)
            widgetLayout.addStretch()
            widgetLayout.setAlignment(QtCore.Qt.AlignCenter)

            #add widget to QListView
            widget.setLayout(widgetLayout)
            widget.setFixedSize(self.WIDTH, self.HEIGHT)
            widget.setParent(self)
            self._child_widgets.append(widget)

        self._move_panels()

    def _move_panels(self):
        num_per_row = max(int((self.width()) / self.WIDTH), 1)

        for i in range(len(self.qid_list)):
            y = int(i / num_per_row)
            x = i % num_per_row
            self._child_widgets[i].move(x * self.WIDTH, y * self.HEIGHT)

        # num_rows = math.ceil(8 / float(num_per_row))
        # min_height = num_rows * self.HEIGHT
        # self.setFixedHeight(min_height)

    def delete_question(self, qid):
        remove_index = self.qid_list.index(qid)
        if (remove_index):
            print(qid)
            # del self.qid_list[remove_index]

    def open_question(self, qid):
        print(qid)
        return


    def clear_questions(self): #TODO
        return


    def resizeEvent(self, QResizeEvent):
        self._move_panels()


if __name__ == '__main__':
#    import callback_fix
    app = QApplication(sys.argv)
    gui = QuestionManagerWidget()
    gui.show()
    app.exec_()

