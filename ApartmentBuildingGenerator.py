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
        self.main_layout = QtWidgets.QVBoxLayout()
        # Make parameter UI
        self.make_dimensions_options_ui()  # length, width, height
        # self.make_details_options_ui()  # balconies, awnings, etc.
        self.make_buttons_ui()  # Build and Cancel buttons
        self.setLayout(self.main_layout)
        self._connect_signals()

    def make_dimensions_options_ui(self):
        self.dimensions_options_header_layout = QtWidgets.QHBoxLayout()
        self.dimensions_lbl = QtWidgets.QLabel("Dimensions")
        self.dimensions_options_header_layout.addWidget(self.dimensions_lbl)
        self.main_layout.addLayout(self.dimensions_options_header_layout)

        self.width_option_layout = QtWidgets.QHBoxLayout()
        self.length_option_layout = QtWidgets.QHBoxLayout()
        self.height_option_layout = QtWidgets.QHBoxLayout()

        self.width_lbl = QtWidgets.QLabel("Width")
        self.length_lbl = QtWidgets.QLabel("Length")
        self.height_lbl = QtWidgets.QLabel("Height")

        self.width_spinbox = QtWidgets.QSpinBox()
        self.width_spinbox.setSingleStep(1)
        self.width_spinbox.setValue(4)
        self.width_spinbox.setMinimum(2)
        self.width_spinbox.setMaximum(100)
        self.width_option_layout.addWidget(self.width_lbl)
        self.width_option_layout.addWidget(self.width_spinbox)

        self.length_spinbox = QtWidgets.QSpinBox()
        self.length_spinbox.setSingleStep(1)
        self.length_spinbox.setValue(2)
        self.length_spinbox.setMinimum(2)
        self.length_spinbox.setMaximum(100)
        self.length_option_layout.addWidget(self.length_lbl)
        self.length_option_layout.addWidget(self.length_spinbox)

        self.height_spinbox = QtWidgets.QSpinBox()
        self.height_spinbox.setSingleStep(1)
        self.height_spinbox.setValue(3)
        self.height_spinbox.setMinimum(1)
        self.height_spinbox.setMaximum(100)
        self.height_option_layout.addWidget(self.height_lbl)
        self.height_option_layout.addWidget(self.height_spinbox)

        self.main_layout.addLayout(self.width_option_layout)
        self.main_layout.addLayout(self.length_option_layout)
        self.main_layout.addLayout(self.height_option_layout)

    def make_buttons_ui(self):
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.main_layout.addWidget(self.build_btn)
        self.main_layout.addWidget(self.cancel_btn)

    def build(self):
        print("Build")
