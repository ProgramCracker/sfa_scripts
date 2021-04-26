import logging
import random

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class QTTesting(QtWidgets.QDialog):

    def __init__(self):
        super(QTTesting, self).__init__(parent=maya_main_window())
        self.setWindowTitle("QT_Testing")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)

        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.selection()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Test UI")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.lists = self.list_of_Selected()
        self.boxes = self.checkBoxes()

        self.main_lay = QtWidgets.QGridLayout()
        self.main_lay.setColumnMinimumWidth(3, 200)
        self.main_lay.addWidget(self.title_lbl, 0, 0)
        self.main_lay.addLayout(self.boxes, 2, 0)
        self.main_lay.addLayout(self.lists, 3, 0)
        self.setLayout(self.main_lay)

    def list_of_Selected(self):
        layout = QtWidgets.QHBoxLayout()
        self.selected_list = QtWidgets.QListWidget()
        self.targetList = QtWidgets.QListWidget()
        first = "dog"
        second = "cat"
        third = "monkey"
        self.selected_list.addItem(first)
        self.selected_list.addItem(second)
        self.targetList.addItem(third)
        layout.addWidget(self.selected_list, 0, 0)
        layout.addWidget(self.targetList, 0, 1)

        return layout

    def checkBoxes(self):
        layout = QtWidgets.QHBoxLayout()
        self.first_box = QtWidgets.QCheckBox("First List")
        self.second_box = QtWidgets.QCheckBox("Second List")
        self.first_box.setChecked(True)

        layout.addWidget(self.first_box, 0, 0)
        layout.addWidget(self.second_box, 0, 0)

        return layout

    def selection(self):
        if self.first_box.isChecked():
            self.selected = cmds.ls(orderedSelection=True)
            self.selected_list.addItems(self.selected)

            # if self.selected == 1():
            #     cmds.warning("select target objects")
            # else:
            #
        else:
            cmds.warning("Choose a check box")

    # while True:
    #     if cmds.ls(selection=True) +:
    #         self.selection()
    #     else:
    #         cmds.warning("Selected some shapes")
