import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance


def get_maya_main_win():
    """Return the Maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win_addr), QtWidgets.QWidget)


class Window(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.setWindowTitle("Apartment Building Generator")
        self.resize(500, 200)
        self._mk_main_layout()

    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.build_btn.clicked.connect(self.build)

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()  # vertical layout
        # Make parameter UI
        self.make_buttons_ui()  # Build and Cancel buttons
        self.setLayout(self.main_layout)
        self._connect_signals()

    def make_buttons_ui(self):
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.main_layout.addWidget(self.build_btn)
        self.main_layout.addWidget(self.cancel_btn)

    def build(self):
        print("Build")
