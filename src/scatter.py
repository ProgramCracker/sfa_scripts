from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class Instancing(object):

    def __init__(self):
        self.scatter = ScatterTool()

        self.instance_on = self.scatter.select[0]
        self.to_be_instanced = self.scatter.select[1]
        self.time_to_instance()

    def time_to_instance(self):
        for i in self._get_vertices():
            new_instance = cmds.instance(self.to_be_instanced)
            # position = cmds.setAttr('self.new_instance.translateX')

            cmds.move(i.x, i.y, i.z, new_instance)

        # if self.scatter.vertex_chkBox.isChecked():
            # for i in self._get_vertices():
                # new_instance = cmds.instance(self.to_be_instanced)
                # position = cmds.setAttr('self.new_instance.translateX')

                # cmds.move(i.x, i.y, i.z, new_instance)
        # elif self.scatter.face_chkBox.isChecked():
            # print {"nah"}
        # else:
            # print{"none"}

    def _get_vertices(self):
        self.target = self.instance_on
        list = cmds.ls(self.instance_on)
        for item in list:
            vertice_num = cmds.polyEvaluate(v=True)
            cmds.select(cl=True)
            cmds.select(item + '.vtx[0:' + str(vertice_num) + ']',
                        add=True)
            vertexnames = cmds.filterExpand(sm=31)
            return vertexnames


class ScatterTool(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterTool, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(1000)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.select = cmds.ls(orderedSelection=True)
        self.ran_xmin_scale = 1
        self.ran_xmax_scale = 1
        self.ran_ymin_scale = 1
        self.ran_ymax_scale = 1
        self.ran_zmin_scale = 1
        self.ran_zmax_scale = 1

        self.ran_xmin_rot = 1
        self.ran_xmax_rot = 1
        self.ran_ymin_rot = 1
        self.ran_ymax_rot = 1
        self.ran_zmin_rot = 1
        self.ran_zmax_rot = 1

        self.create_ui()

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
        self.time_to_instance()

    def time_to_instance(self):
        for i in self._get_vertices():
            new_instance = cmds.instance(self.select[1])

            cmds.move(i.x, i.y, i.z, new_instance)

    # def _get_vertices(self):
        # self.target = self.select[0]
        # list = cmds.ls(self.select[0])
        # for item in list:
           # vertice_num = cmds.polyEvaluate(v=True)
           # cmds.select(cl=True)
           # cmds.select(item + '.vtx[0:' + str(vertice_num) + ']',
                        #add=True)
           # vertexnames = cmds.filterExpand(sm=31)
            #return vertexnames

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
        self.face_chkBox = QtWidgets.QCheckBox("Faces")

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

        self.x_min = QtWidgets.QSpinBox()
        self.x_min.setFixedWidth(50)
        self.x_min.setValue(self.ran_xmin_scale)

        self.x_max = QtWidgets.QSpinBox()
        self.x_max.setFixedWidth(50)
        self.x_max.setValue(self.ran_xmax_scale)

        self.y_min = QtWidgets.QSpinBox()
        self.y_min.setFixedWidth(50)
        self.y_min.setValue(self.ran_ymin_scale)

        self.y_max = QtWidgets.QSpinBox()
        self.y_max.setFixedWidth(50)
        self.y_max.setValue(self.ran_ymax_scale)

        self.z_min = QtWidgets.QSpinBox()
        self.z_min.setFixedWidth(50)
        self.z_min.setValue(self.ran_zmin_scale)

        self.z_max = QtWidgets.QSpinBox()
        self.z_max.setFixedWidth(50)
        self.z_max.setValue(self.ran_zmax_scale)

        layout.addWidget(self.scale_header_lbl, 0, 0, 1, -1)
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

        self.x_min = QtWidgets.QSpinBox()
        self.x_min.setFixedWidth(50)
        self.x_min.setValue(self.ran_xmin_rot)

        self.x_max = QtWidgets.QSpinBox()
        self.x_max.setFixedWidth(50)
        self.x_max.setValue(self.ran_xmax_rot)

        self.y_min = QtWidgets.QSpinBox()
        self.y_min.setFixedWidth(50)
        self.y_min.setValue(self.ran_ymin_rot)

        self.y_max = QtWidgets.QSpinBox()
        self.y_max.setFixedWidth(50)
        self.y_max.setValue(self.ran_ymax_rot)

        self.z_min = QtWidgets.QSpinBox()
        self.z_min.setFixedWidth(50)
        self.z_min.setValue(self.ran_zmin_rot)

        self.z_max = QtWidgets.QSpinBox()
        self.z_max.setFixedWidth(50)
        self.z_max.setValue(self.ran_zmax_rot)

        layout.addWidget(self.scale_header_lbl, 0, 0, 1, -1)
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
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout
