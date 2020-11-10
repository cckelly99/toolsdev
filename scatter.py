import random
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def maya_main_window():
    """Return Maya Main Window Widget"""
    if __name__ == '__main__':
        main_window = omui.MQtUtilWindow()
        return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatter_tool = ScatterTool()
        self.create_ui()
        self.create_connections()

    def create_connections(self):
        """Connects Signals and Slots"""
        self.scatter_push_btn.clicked.connect(self._scatter_object)
        self.ots_button.clicked.connect(self._choose_objects)

        self.add_rot_btn.clicked.connect(self._add_min_rot)
        self.subtract_rot_btn.clicked.connect(self._subtract_min_rot)
        self.add_max_rot_btn.clicked.connect(self._add_max_rot)
        self.subtract_max_rot_btn.clicked.connect(self._subtract_max_rot)

        self.add_den_btn.clicked.connect(self._add_den)
        self.subtract_den_btn.clicked.connect(self._subtract_den)


    @QtCore.Slot()
    def _scatter_object(self):
        """Scatters the object based on the values set"""
        self.min_scale = self.min_scale_sbx.value()
        self.max_scale = self.max_scale_sbx.value()
        self.min_rot = self.min_rot_sbx.value()
        self.max_rot = self.max_rot_sbx.value()
        self.density = self.density_sbx.value()

        self.scatter_tool.scatter(self.min_scale, self.max_scale,
                                  self.min_rot, self.max_rot, self.density)

    @QtCore.Slot()
    def _choose_objects(self):
        """Selects and sets objects"""
        self.ots_layout.setText(self.scatter_tool.set_scatter_object())
        self.os_layout.setText(self.scatter_tool.set_scatter_base())

    @QtCore.Slot()
    def _add_min_rot(self):
        self.min_rot_sbx.setValue(self.min_rot_sbx.value() + 10)

    @QtCore.Slot()
    def _subtract_min_rot(self):
        self.min_rot_sbx.setValue(self.min_rot_sbx.value() - 10)

    @QtCore.Slot()
    def _add_max_rot(self):
        self.max_rot_sbx.setValue(self.max_rot_sbx.value() + 10)

    @QtCore.Slot()
    def _subtract_max_rot(self):
        self.max_rot_sbx.setValue(self.max_rot_sbx.value() - 10)

    @QtCore.Slot()
    def _add_den(self):
        self.density_sbx.setValue(self.density_sbx.value() + 10)

    @QtCore.Slot()
    def _subtract_den(self):
        self.density_sbx.setValue(self.density_sbx.value() - 10)

    def create_ui(self):
        """Puts Together UI"""
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")

        self.object_to_scatter_layout = self._ots_layout()
        self.scale_name = QtWidgets.QLabel("Set Min/Max Scale")
        self.scale_name.setAlignment(QtCore.Qt.AlignCenter)
        self.scale_name.setStyleSheet("font: bold 10px")
        self.scale_boxes = self._scale_box_layout()
        self.rot_name = QtWidgets.QLabel("Set Min/Max Rotation")
        self.rot_name.setAlignment(QtCore.Qt.AlignCenter)
        self.rot_name.setStyleSheet("font: bold 10px")
        self.rot_boxes = self._rotation_box_layout()
        self.density_layout = self._density_layout()
        self.scatter_push_btn = QtWidgets.QPushButton("Scatter Objects")

        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.object_to_scatter_layout)
        self.main_lay.addWidget(self.scale_name)
        self.main_lay.addLayout(self.scale_boxes)
        self.main_lay.addWidget(self.rot_name)
        self.main_lay.addLayout(self.rot_boxes)
        self.main_lay.addLayout(self.density_layout)
        self.main_lay.addWidget(self.scatter_push_btn)
        self.setLayout(self.main_lay)

    def _ots_layout(self):
        """Displays object to scatter"""
        self.ots_layout = QtWidgets.QLineEdit("Object to Scatter")
        self.os_layout = QtWidgets.QLineEdit("Object to Scatter on")
        self.ots_button = QtWidgets.QPushButton("Choose Selected Objects")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.ots_layout)
        layout.addWidget(self.os_layout)
        layout.addWidget(self.ots_button)
        return layout

    def _scale_box_layout(self):
        self.min_scale_sbx = QtWidgets.QDoubleSpinBox()
        self.max_scale_sbx = QtWidgets.QDoubleSpinBox()
        self.min_scale_sbx.setFixedWidth(100)
        self.max_scale_sbx.setFixedWidth(100)
        self.min_scale_sbx.setMinimum(0.1)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.min_scale_sbx)
        layout.addWidget(self.max_scale_sbx)
        return layout

    def _rotation_box_layout(self):
        self.min_rot_sbx = QtWidgets.QDoubleSpinBox()
        self.max_rot_sbx = QtWidgets.QDoubleSpinBox()
        self.add_rot_btn = QtWidgets.QPushButton("+10")
        self.subtract_rot_btn = QtWidgets.QPushButton("-10")
        self.add_max_rot_btn = QtWidgets.QPushButton("+10")
        self.subtract_max_rot_btn = QtWidgets.QPushButton("-10")
        self.min_rot_sbx.setFixedWidth(100)
        self.max_rot_sbx.setFixedWidth(100)
        self.min_rot_sbx.setRange(0.0, 360.0)
        self.max_rot_sbx.setRange(0.0, 360.0)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.subtract_rot_btn)
        layout.addWidget(self.min_rot_sbx)
        layout.addWidget(self.add_rot_btn)

        layout.addWidget(self.subtract_max_rot_btn)
        layout.addWidget(self.max_rot_sbx)
        layout.addWidget(self.add_max_rot_btn)
        return layout

    def _density_layout(self):
        self.density_name = QtWidgets.QLabel("Set Scatter Density")
        self.density_sbx = QtWidgets.QSpinBox()
        self.add_den_btn = QtWidgets.QPushButton("+10")
        self.subtract_den_btn = QtWidgets.QPushButton("-10")
        self.density_sbx.setFixedWidth(50)
        self.density_sbx.setRange(1, 100)

        sbx_layout = QtWidgets.QHBoxLayout()
        sbx_layout.addWidget(self.add_den_btn)
        sbx_layout.addWidget(self.subtract_den_btn)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.density_name)
        layout.addLayout(sbx_layout)
        return layout


class ScatterTool:
    def __init__(self):
        self.scatter_object_name = "Scatter Object"
        self.scatter_base = []

    def scatter(self, min_scale, max_scale, min_rotation, max_rotation,
                scatter_density):

        selection = cmds.ls(orderedSelection=True, flatten=True)
        vertex_names = cmds.filterExpand(selection, selectionMask=31,
                                         expand=True)
        object_to_instance = selection[0]

        scatter_percent = scatter_density / 100.00
        scatter_list_size = int((len(vertex_names) * scatter_percent))
        percent_vertex_names = random.sample(vertex_names, scatter_list_size)

        if cmds.objectType(object_to_instance, isType="transform"):
            for vertex in percent_vertex_names:
                new_instance = cmds.instance(object_to_instance)

                instance_scale = random.uniform(min_scale, max_scale)
                cmds.scale(instance_scale, instance_scale, instance_scale,
                           new_instance)

                instance_rotation = random.uniform(min_rotation, max_rotation)
                cmds.rotate(instance_rotation, instance_rotation,
                            instance_rotation, new_instance)

                position_vector = cmds.pointPosition(vertex, world=True)
                cmds.move(position_vector[0], position_vector[1],
                          position_vector[2], new_instance, absolute=True,
                          worldSpace=True)
        else:
            print("Please ensure the first object you select is a transform.")

    def set_scatter_object(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        object_to_instance = selection[0]
        self.scatter_object_name = object_to_instance
        return object_to_instance

    def set_scatter_base(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        vertex_names = cmds.filterExpand(selection, selectionMask=31,
                                         expand=True)
        self.scatter_base = vertex_names
        return selection[1]
