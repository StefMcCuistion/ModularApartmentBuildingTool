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
        self.make_details_options_ui()  # balconies, awnings, etc.
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

    def make_details_options_ui(self):
        # header
        self.details_options_header_layout = QtWidgets.QHBoxLayout()
        self.details_lbl = QtWidgets.QLabel("Details")
        self.details_options_header_layout.addWidget(self.details_lbl)
        self.main_layout.addLayout(self.details_options_header_layout)

        # door placement (drives int 0 to width -1)
        self.door_placement_layout = QtWidgets.QHBoxLayout()
        self.door_placement_lbl = QtWidgets.QLabel("Door Placement")
        self.door_placement_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.door_placement_slider.setMinimum(0)
        self.door_placement_slider.setMaximum(100)
        self.door_placement_slider.setValue(0)
        self.door_placement_layout.addWidget(self.door_placement_lbl)
        self.door_placement_layout.addWidget(self.door_placement_slider)
        self.main_layout.addLayout(self.door_placement_layout)

        # awning density
        self.awning_density_layout = QtWidgets.QHBoxLayout()
        self.awning_density_lbl = QtWidgets.QLabel("Awning Density")
        self.awning_density_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.awning_density_slider.setMinimum(0)
        self.awning_density_slider.setMaximum(100)
        self.awning_density_slider.setValue(40)
        self.awning_density_layout.addWidget(self.awning_density_lbl)
        self.awning_density_layout.addWidget(self.awning_density_slider)
        self.main_layout.addLayout(self.awning_density_layout)

        # balcony density
        self.balcony_density_layout = QtWidgets.QHBoxLayout()
        self.balcony_density_lbl = QtWidgets.QLabel("Balcony Density")
        self.balcony_density_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.balcony_density_slider.setMinimum(0)
        self.balcony_density_slider.setMaximum(100)
        self.balcony_density_slider.setValue(80)
        self.balcony_density_layout.addWidget(self.balcony_density_lbl)
        self.balcony_density_layout.addWidget(self.balcony_density_slider)
        self.main_layout.addLayout(self.balcony_density_layout)

        # smokestacks
        self.smokestacks_layout = QtWidgets.QHBoxLayout()
        self.smokestacks_lbl = QtWidgets.QLabel("Smokestacks")
        self.smokestacks_checkbox = QtWidgets.QCheckBox()
        self.smokestacks_checkbox.setChecked(True)
        self.smokestacks_layout.addWidget(self.smokestacks_lbl)
        self.smokestacks_layout.addWidget(self.smokestacks_checkbox)
        self.main_layout.addLayout(self.smokestacks_layout)

        # sidewalk
        self.sidewalk_layout = QtWidgets.QHBoxLayout()
        self.sidewalk_lbl = QtWidgets.QLabel("Sidewalk")
        self.sidewalk_checkbox = QtWidgets.QCheckBox()
        self.sidewalk_checkbox.setChecked(True)
        self.sidewalk_layout.addWidget(self.sidewalk_lbl)
        self.sidewalk_layout.addWidget(self.sidewalk_checkbox)
        self.main_layout.addLayout(self.sidewalk_layout)

    def make_buttons_ui(self):
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.main_layout.addWidget(self.build_btn)
        self.main_layout.addWidget(self.cancel_btn)

    def build(self):
        self.cleanup()  # delete old building

        # init attributes
        self.building_height = self.height_spinbox.value()
        self.building_width = self.width_spinbox.value()
        self.building_length = self.length_spinbox.value()

        # cell dimensions for cell lattice
        self.cell_width = 340  # cm
        self.cell_height = 290

        # master group
        cmds.group(em=True, name="SM_ApartmentBuilding")

        # floor groups
        for floor in range(self.building_height):
            cmds.group(em=True, name=f"floor_{floor+1}")

        # nested loops to create cell lattice
        for x in range(self.building_width):
            for y in range(self.building_height):
                for z in range(self.building_length):
                    # create cell
                    cell_obj_name = cmds.polyCube(w=self.cell_width,
                                                  h=self.cell_height,
                                                  d=self.cell_width)[0]
                    # move cell to position in lattice
                    cmds.move(x*self.cell_width,
                              y*self.cell_height+.5*self.cell_height,
                              z*self.cell_width)
                    # group cell under floor group
                    cmds.parent(cell_obj_name, f"floor_{y+1}")
                # group floor under master group
                cmds.parent(f"floor_{y+1}", "SM_ApartmentBuilding")

    def cleanup(self):
        if cmds.objExists("SM_ApartmentBuilding"):
            cmds.delete("SM_ApartmentBuilding")