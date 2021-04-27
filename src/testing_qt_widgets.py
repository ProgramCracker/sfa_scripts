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
        self.creating_connections()
        self.function = functional()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Test UI")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.lists = self.list_of_Selected()
        self.boxes = self.buttons()

        self.main_lay = QtWidgets.QGridLayout()
        self.main_lay.setColumnMinimumWidth(3, 200)
        self.main_lay.addWidget(self.title_lbl, 0, 0)
        self.main_lay.addLayout(self.boxes, 2, 0)
        self.main_lay.addLayout(self.lists, 3, 0)
        self.setLayout(self.main_lay)

    def creating_connections(self):
        self.first_btn.clicked.connect(self.update_first)
        self.second_btn.clicked.connect(self.update_second)

    @QtCore.Slot()
    def update_first(self):
        cmds.warning("clicked button")
        self.function.update_locations()
        self.selected_list.clear()
        for object in self.function.update_locations():
            self.selected_list.addItem(object)
            cmds.warning("putting object in")
        self.selected_list.update()

    @QtCore.Slot()
    def update_second(self):
        self.function.update_targets_to_instance()
        self.target_list.clear()
        for object in self.function.update_targets_to_instance():
            self.target_list.addItem(object)
        self.target_list.update()

    def list_of_Selected(self):
        layout = QtWidgets.QHBoxLayout()
        self.selected_list = QtWidgets.QListWidget()
        self.target_list = QtWidgets.QListWidget()
        first = "dog"
        second = "cat"
        third = "monkey"
        self.selected_list.addItem(first)
        self.selected_list.addItem(second)
        self.target_list.addItem(third)
        layout.addWidget(self.selected_list, 0, 0)
        layout.addWidget(self.target_list, 0, 1)

        return layout

    def buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.first_btn = QtWidgets.QPushButton("Update Selection")
        self.second_btn = QtWidgets.QPushButton("Update Selection")

        layout.addWidget(self.first_btn)
        layout.addWidget(self.second_btn)

        return layout


class functional(object):

    def __init__(self):
        self.selected = cmds.ls(selection=True)

        self.instance_list = []
        self.instance_locations = []

    def update_locations(self):
        new_list = cmds.ls(selection=True)
        self.instance_locations = new_list

        return self.instance_locations

    def update_targets_to_instance(self):
        new_list = cmds.ls(selection=True)
        self.instance_list = new_list

        return self.instance_list