import logging
import random

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc

log = logging.getLogger(__name__)

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterTool(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterTool, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.select = cmds.ls(orderedSelection=True)

        self.instance = Instancing()
        self.create_ui()
        self.creating_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Super Scatter Tool 9000")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.button_lay = self._create_button_ui()
        self.select_lay = self._create_selection_ui()
        self.scale_lay = self._create_randomscale_ui()
        self.position_lay = self._create_randomposition_ui()
        self.chkBox_lay = self._create_checkbox_ui()

        self.main_lay = QtWidgets.QGridLayout()
        self.main_lay.setColumnMinimumWidth(3, 200)
        self.main_lay.addWidget(self.title_lbl, 0, 0)
        self.main_lay.addLayout(self.select_lay, 2, 0)
        self.main_lay.addLayout(self.chkBox_lay, 3, 0)
        self.main_lay.addLayout(self.scale_lay, 2, 3)
        self.main_lay.addLayout(self.position_lay, 3, 3)
        self.main_lay.addLayout(self.button_lay, 4, 3)
        self.setLayout(self.main_lay)

    def creating_connections(self):
        self.scatter_btn.clicked.connect(self.scatter)

    @QtCore.Slot()
    def scatter(self):
        self._set_properties_from_ui()
        if self.vertex_chkBox.isChecked():
            self.instance.time_to_instance_on_vertices()
        elif self.face_chkBox.isChecked():
            cmds.warning("The faces feature isn't added yet. Use the"
                         " vertices check box.")
        else:
            cmds.warning("Please choose a check box.")


    def _create_selection_ui(self):
        self.target_header_lbl = QtWidgets.QLabel("Target Object to"
                                                  " Instance On")
        self.surface_le = QtWidgets.QLineEdit(self.select[0])
        self.instance_header_lbl = QtWidgets.QLabel("Object to "
                                                    "Instance")
        self.int_obj_le = QtWidgets.QLineEdit(self.select[1])
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.target_header_lbl)
        layout.addWidget(self.surface_le)
        layout.addWidget(self.instance_header_lbl)
        layout.addWidget(self.int_obj_le)
        return layout

    def _create_checkbox_ui(self):
        self.group_header_lbl = QtWidgets.QLabel("Instances will appear"
                                                 " on?")
        self.group_header_lbl.setStyleSheet("font: 20px")
        self.vertex_chkBox = QtWidgets.QCheckBox("Vertices")
        self.vertex_chkBox.isChecked()
        self.face_chkBox = QtWidgets.QCheckBox("Faces (Non-Functional)")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.group_header_lbl)
        layout.addWidget(self.vertex_chkBox)
        layout.addWidget(self.face_chkBox)

        return layout

    def _create_randomscale_ui(self):
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

        self.x_min_s = QtWidgets.QSpinBox()
        self.x_min_s.setFixedWidth(50)
        self.x_min_s.setValue(self.instance.r_xmn_s)
        self.x_min_s.setRange(0.1, 100.)

        self.x_max_s = QtWidgets.QSpinBox()
        self.x_max_s.setFixedWidth(50)
        self.x_max_s.setValue(self.instance.r_xmx_s)
        self.x_max_s.setRange(0.1, 100.)

        self.y_min_s = QtWidgets.QSpinBox()
        self.y_min_s.setFixedWidth(50)
        self.y_min_s.setValue(self.instance.r_ymn_s)
        self.y_min_s.setRange(0.1, 100.)

        self.y_max_s = QtWidgets.QSpinBox()
        self.y_max_s.setFixedWidth(50)
        self.y_max_s.setValue(self.instance.r_ymx_s)
        self.y_max_s.setRange(0.1, 100.)

        self.z_min_s = QtWidgets.QSpinBox()
        self.z_min_s.setFixedWidth(50)
        self.z_min_s.setValue(self.instance.r_zmn_s)
        self.z_min_s.setRange(0.1, 100.)

        self.z_max_s = QtWidgets.QSpinBox()
        self.z_max_s.setFixedWidth(50)
        self.z_max_s.setValue(self.instance.r_zmx_s)
        self.z_max_s.setRange(0.1, 100.)

        layout.addWidget(self.scale_header_lbl, 0, 0, 1, -1)
        layout.addWidget(self.min_lin_header, 1, 0)
        layout.addWidget(self.max_lin_header, 2, 0)

        layout.addWidget(self.x_min_s, 1, 1)
        layout.addWidget(self.x_max_s, 2, 1)
        layout.addWidget(self.x_lbl, 1, 2)
        layout.addWidget(self.x_lbl_2, 2, 2)

        layout.addWidget(self.y_min_s, 1, 4)
        layout.addWidget(self.y_max_s, 2, 4)
        layout.addWidget(self.y_lbl, 1, 5)
        layout.addWidget(self.y_lbl_2, 2, 5)

        layout.addWidget(self.z_min_s, 1, 7)
        layout.addWidget(self.z_max_s, 2, 7)
        layout.addWidget(self.z_lbl, 1, 8)
        layout.addWidget(self.z_lbl_2, 2, 8)

        return layout

    def _create_randomposition_ui(self):
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

        self.x_min_r = QtWidgets.QSpinBox()
        self.x_min_r.setFixedWidth(50)
        self.x_min_r.setValue(self.instance.r_xmn_r)
        self.x_min_r.setRange(0, 360)

        self.x_max_r = QtWidgets.QSpinBox()
        self.x_max_r.setFixedWidth(50)
        self.x_max_r.setValue(self.instance.r_xmx_r)
        self.x_max_r.setRange(0, 360)

        self.y_min_r = QtWidgets.QSpinBox()
        self.y_min_r.setFixedWidth(50)
        self.y_min_r.setValue(self.instance.r_ymn_r)
        self.y_min_r.setRange(0, 360)

        self.y_max_r = QtWidgets.QSpinBox()
        self.y_max_r.setFixedWidth(50)
        self.y_max_r.setValue(self.instance.r_ymx_r)
        self.y_max_r.setRange(0, 360)

        self.z_min_r = QtWidgets.QSpinBox()
        self.z_min_r.setFixedWidth(50)
        self.z_min_r.setValue(self.instance.r_zmn_r)
        self.z_min_r.setRange(0, 360)

        self.z_max_r = QtWidgets.QSpinBox()
        self.z_max_r.setFixedWidth(50)
        self.z_max_r.setValue(self.instance.r_zmx_r)
        self.z_max_r.setRange(0, 360)

        layout.addWidget(self.scale_header_lbl, 0, 0, 1, -1)
        layout.addWidget(self.min_lin_header, 1, 0)
        layout.addWidget(self.max_lin_header, 2, 0)

        layout.addWidget(self.x_min_r, 1, 1)
        layout.addWidget(self.x_max_r, 2, 1)
        layout.addWidget(self.x_lbl, 1, 2)
        layout.addWidget(self.x_lbl_2, 2, 2)

        layout.addWidget(self.y_min_r, 1, 4)
        layout.addWidget(self.y_max_r, 2, 4)
        layout.addWidget(self.y_lbl, 1, 5)
        layout.addWidget(self.y_lbl_2, 2, 5)

        layout.addWidget(self.z_min_r, 1, 7)
        layout.addWidget(self.z_max_r, 2, 7)
        layout.addWidget(self.z_lbl, 1, 8)
        layout.addWidget(self.z_lbl_2, 2, 8)

        return layout

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _set_properties_from_ui(self):
        self.instance.r_xmn_s = self.x_min_s.value()
        self.instance.r_xmx_s = self.x_max_s.value()
        self.instance.r_ymn_s = self.y_min_s.value()
        self.instance.r_ymn_s = self.y_max_s.value()
        self.instance.r_zmn_s = self.z_min_s.value()
        self.instance.r_zmx_s = self.z_min_s.value()

        self.instance.r_xmn_r = self.x_min_r.value()
        self.instance.r_xmx_r = self.x_max_r.value()
        self.instance.r_ymn_r = self.y_min_r.value()
        self.instance.r_ymx_r = self.y_max_r.value()
        self.instance.r_zmn_r = self.z_min_r.value()
        self.instance.r_zmx_r = self.z_max_r.value()


class Instancing(object):

    def __init__(self):

        self.r_xmn_s = 1
        self.r_xmx_s = 1
        self.r_ymn_s = 1
        self.r_ymx_s = 1
        self.r_zmn_s = 1
        self.r_zmx_s = 1

        self.xScl = random.uniform(self.r_xmn_s, self.r_xmx_s)
        self.yScl = random.uniform(self.r_ymn_s, self.r_ymx_s)
        self.zScl = random.uniform(self.r_zmn_s, self.r_zmx_s)

        self.r_xmn_r = 1
        self.r_xmx_r = 90
        self.r_ymn_r = 1
        self.r_ymx_r = 90
        self.r_zmn_r = 1
        self.r_zmx_r = 90

        self.xRot = random.uniform(self.r_xmn_r, self.r_xmx_r)
        self.yRot = random.uniform(self.r_ymn_r, self.r_ymx_r)
        self.zRot = random.uniform(self.r_zmn_r, self.r_zmx_r)

        self.selected = cmds.ls(orderedSelection=True)

        self.instance_on = self.selected[0]
        self.to_be_instanced = self.selected[1]

    def time_to_instance_on_vertices(self):
        for vert in self._get_vertices():
            pos = cmds.pointPosition(vert)
            new_instance = cmds.instance(self.to_be_instanced)
            cmds.move(pos[0], pos[1], pos[2], new_instance)

            self.xScl = random.uniform(self.r_xmn_s, self.r_xmx_s)
            self.yScl = random.uniform(self.r_ymn_s, self.r_ymx_s)
            self.zScl = random.uniform(self.r_zmn_s, self.r_zmx_s)

            cmds.scale(self.xScl, self.yScl, self.zScl, new_instance)

            self.xRot = random.uniform(self.r_xmn_r, self.r_xmx_r)
            self.yRot = random.uniform(self.r_ymn_r, self.r_ymx_r)
            self.zRot = random.uniform(self.r_zmn_r, self.r_zmx_r)

            cmds.rotate(self.xRot, self.yRot, self.zRot, new_instance)
        return

    def _get_vertices(self):
        self.target = self.instance_on
        selected_mesh = cmds.ls(self.target, flatten=True)
        selected_verts = cmds.polyListComponentConversion(selected_mesh,
                                                          toVertex=True)
        selected_verts = cmds.filterExpand(selected_verts,
                                           selectionMask=31)
        return selected_verts
