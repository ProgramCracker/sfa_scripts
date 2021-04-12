from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class ScatterTool(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterTool, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(1000)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_UI()

    def create_UI(self):
        self.title_lbl = QtWidgets.QLabel("Super Scatter Tool 9000")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.button_lay = self._create_button_ui()
        self.select_lay = self._create_selection_ui()
        self.scale_lay = self._create_randomScale_ui()
        self.position_lay = self._create_randomPosition_ui()
        self.chkBox_lay = self._create_checkBox_ui()

        self.main_lay = QtWidgets.QGridLayout()
        self.main_lay.setColumnMinimumWidth(3, 200)
        self.main_lay.addWidget(self.title_lbl, 0, 0)
        self.main_lay.addLayout(self.select_lay, 2, 0)
        self.main_lay.addLayout(self.chkBox_lay, 3, 0)
        self.main_lay.addLayout(self.scale_lay, 2, 3)
        self.main_lay.addLayout(self.position_lay, 3, 3)
        self.main_lay.addLayout(self.button_lay, 4, 3)
        self.setLayout(self.main_lay)


    def _create_selection_ui(self):
        self.target_header_lbl = QtWidgets.QLabel("Target Object to"
                                                  " Instance On")
        self.surface_le = QtWidgets.QLineEdit()
        self.instance_header_lbl = QtWidgets.QLabel("Object to "
                                                    "Instance")
        self.int_obj_le = QtWidgets.QLineEdit()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.target_header_lbl)
        layout.addWidget(self.surface_le)
        layout.addWidget(self.instance_header_lbl)
        layout.addWidget(self.int_obj_le)
        return layout


    def _create_checkBox_ui(self):
        self.group_header_lbl = QtWidgets.QLabel("Instances will appear"
                                                 " on?")
        self.group_header_lbl.setStyleSheet("font: 20px")
        self.vertex_chkBox = QtWidgets.QCheckBox("Vertices")
        self.face_chkBox = QtWidgets.QCheckBox("Faces")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.group_header_lbl)
        layout.addWidget(self.vertex_chkBox)
        layout.addWidget(self.face_chkBox)

        return layout


    def _create_randomScale_ui(self):
        #self.groupbox = QtWidgets.QGroupBox("Random Scale")
        layout = QtWidgets.QGridLayout()
        self.scale_header_lbl = QtWidgets.QLabel("Scale Randomization")
        self.scale_header_lbl.setStyleSheet("font: 20px")
        self.min_lin_header = QtWidgets.QLabel("Min")
        self.max_lin_header = QtWidgets.QLabel("Max")
        self.x_lbl = QtWidgets.QLabel("x")
        self.y_lbl = QtWidgets.QLabel("y")
        self.z_lbl = QtWidgets.QLabel("z")
        self.x_lbl_2 = QtWidgets.QLabel("x")
        self.y_lbl_2 = QtWidgets.QLabel("y")
        self.z_lbl_2 = QtWidgets.QLabel("z")


        self.x_min = QtWidgets.QSpinBox()
        self.x_min.setFixedWidth(50)
        self.x_min.setValue(1)

        self.x_max = QtWidgets.QSpinBox()
        self.x_max.setFixedWidth(50)
        self.x_max.setValue(1)

        self.y_min = QtWidgets.QSpinBox()
        self.y_min.setFixedWidth(50)
        self.y_min.setValue(1)

        self.y_max = QtWidgets.QSpinBox()
        self.y_max.setFixedWidth(50)
        self.y_max.setValue(1)

        self.z_min = QtWidgets.QSpinBox()
        self.z_min.setFixedWidth(50)
        self.z_min.setValue(1)

        self.z_max = QtWidgets.QSpinBox()
        self.z_max.setFixedWidth(50)
        self.z_max.setValue(1)

        layout.addWidget(self.scale_header_lbl, 0, 0)
        layout.addWidget(self.min_lin_header, 1, 0)
        layout.addWidget(self.max_lin_header, 2, 0)

        layout.addWidget(self.x_min, 1, 1)
        layout.addWidget(self.x_max, 2, 1)
        layout.addWidget(self.x_lbl, 1, 2)
        layout.addWidget(self.x_lbl_2, 2, 2)

        layout.addWidget(self.y_min, 1, 4)
        layout.addWidget(self.y_max, 2, 4)
        layout.addWidget(self.y_lbl, 1, 5)
        layout.addWidget(self.y_lbl_2, 2, 5)

        layout.addWidget(self.z_min, 1, 7)
        layout.addWidget(self.z_max, 2, 7)
        layout.addWidget(self.z_lbl, 1, 8)
        layout.addWidget(self.z_lbl_2, 2, 8)

        return layout




    def _create_randomPosition_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_header_lbl = QtWidgets.QLabel("Rotate"
                                                 " Randomization")
        self.scale_header_lbl.setStyleSheet("font: 20px")
        self.min_lin_header = QtWidgets.QLabel("Min")
        self.max_lin_header = QtWidgets.QLabel("Max")
        self.x_lbl = QtWidgets.QLabel("x")
        self.y_lbl = QtWidgets.QLabel("y")
        self.z_lbl = QtWidgets.QLabel("z")
        self.x_lbl_2 = QtWidgets.QLabel("x")
        self.y_lbl_2 = QtWidgets.QLabel("y")
        self.z_lbl_2 = QtWidgets.QLabel("z")

        self.x_min = QtWidgets.QSpinBox()
        self.x_min.setFixedWidth(50)
        self.x_min.setValue(1)

        self.x_max = QtWidgets.QSpinBox()
        self.x_max.setFixedWidth(50)
        self.x_max.setValue(1)

        self.y_min = QtWidgets.QSpinBox()
        self.y_min.setFixedWidth(50)
        self.y_min.setValue(1)

        self.y_max = QtWidgets.QSpinBox()
        self.y_max.setFixedWidth(50)
        self.y_max.setValue(1)

        self.z_min = QtWidgets.QSpinBox()
        self.z_min.setFixedWidth(50)
        self.z_min.setValue(1)

        self.z_max = QtWidgets.QSpinBox()
        self.z_max.setFixedWidth(50)
        self.z_max.setValue(1)


        layout.addWidget(self.scale_header_lbl, 0, 0)
        layout.addWidget(self.min_lin_header, 1, 0)
        layout.addWidget(self.max_lin_header, 2, 0)

        layout.addWidget(self.x_min, 1, 1)
        layout.addWidget(self.x_max, 2, 1)
        layout.addWidget(self.x_lbl, 1, 2)
        layout.addWidget(self.x_lbl_2, 2, 2)

        layout.addWidget(self.y_min, 1, 4)
        layout.addWidget(self.y_max, 2, 4)
        layout.addWidget(self.y_lbl, 1, 5)
        layout.addWidget(self.y_lbl_2, 2, 5)

        layout.addWidget(self.z_min, 1, 7)
        layout.addWidget(self.z_max, 2, 7)
        layout.addWidget(self.z_lbl, 1, 8)
        layout.addWidget(self.z_lbl_2, 2, 8)

        return layout

    def _create_button_ui(self):
        self.save_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.save_btn)
        return layout