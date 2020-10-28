import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import pymel.core as pmc
from pymel.core.system import Path


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

    def create_ui(self):
        """Puts Together UI"""
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")

        self.object_to_scatter_layout = self._ots_layout()
        self.object_scattered = self._os_layout()

    def _ots_layout(self):
        """Displays object to scatter"""
        self.ots_layout = QtWidgets.QLineEdit("Object to Scatter")
        self.ots_button = QtWidgets.QPushButton("Choose Selected Objects")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.ots_layout)
        layout.addWidget(self.ots_button)
        return layout

    def _os_layout(self):
        """Displays object scattered on"""
        self.os_layout = QtWidgets.QLineEdit("Object to Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.os_layout)
        return layout


class ScatterTool:
    def __init__(self):
        self.scatter_object_name = "Scatter Object"
        self.scatter_base_name = "Scatter Base"

    def scatter(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        vertex_names = cmds.filterExpand(selection, selectionMask=31,
                                         expand=True)
        object_to_instance = selection[0]

        if cmds.objectToInstance(object_to_instance, isType="transform"):
            for vertex in vertex_names:
                new_instance = cmds.instance(object_to_instance)
                position_vector = cmds.pointPosition(vertex, world=True)
                cmds.move(position_vector[0], position_vector[1],
                          position_vector[2], new_instance, absolute=True,
                          worldSpace=True)
        else:
            print("Please ensure the first object you select is a transform.")

    def select_scatter_object(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        object_to_instance = selection[0]
        return object_to_instance

    def select_scatter_base(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        vertex_names = cmds.filterExpand(selection, selectionMask=31,
                                         expand=True)
        return vertex_names
