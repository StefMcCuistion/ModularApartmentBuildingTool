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

    def cleanup(self):
        if cmds.objExists("SM_ApartmentBuilding"):
            cmds.delete("SM_ApartmentBuilding")

    def build(self):
        self.cleanup()  # delete old building

        # init attributes
        self.building_height = self.height_spinbox.value()
        self.building_width = self.width_spinbox.value()
        self.building_length = self.length_spinbox.value()

        # dimensions
        self.cell_width = 340  # cm
        self.cell_height = 290

        self.cornice_height = 160
        self.cornice_overhang = 65

        self.midline_height = 20
        self.midline_overhang = 45

        self.roof_height = 380
        self.roof_depth = 380

        self.master_scale = 1

        # master group
        cmds.group(em=True, name="SM_ApartmentBuilding")

        # roof group
        cmds.group(em=True, name="roof_grp")

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
                                                  d=self.cell_width,
                                                  name=f"cell_{x+1}_{y+1}_{z+1}")[0]
                    # move cell to position in lattice
                    cmds.move(x*self.cell_width,
                              y*self.cell_height+.5*self.cell_height,
                              z*self.cell_width)
                    # group cell under floor group
                    cmds.parent(cell_obj_name, f"floor_{y+1}")
                # group floor under master group
                cmds.parent(f"floor_{y+1}", "SM_ApartmentBuilding")

        # all floor assets:
        # - column
        # - window
        # - balcony
        # - awning
        # top floor assets:
        # - cornice, cornice_corner
        # - roof, roof_corner, rooftop
        # - smokestacks
        # lower floor assets (when floors >= 2):
        # - midline, midline_corner
        # - door

        floor_list = cmds.ls("floor_*")
        max_x = 1
        min_x = 1
        max_z = 1
        min_z = 1

        for floor in floor_list:
            cell_list = cmds.ls(f"{floor}|cell_*")
            print(cell_list)
            # 1st: find extremes
            for cell in cell_list:
                cell_pos = cell.split("_")[1:]
                cell_x = int(cell_pos[0])
                cell_z = int(cell_pos[2])
                max_x = max(max_x, cell_x)
                min_x = min(min_x, cell_x)
                max_z = max(max_z, cell_z)
                min_z = min(min_z, cell_z)
            print(f"highest_cell_x={max_x},"
                  f"lowest_cell_x={min_x},"
                  f"highest_cell_z={max_z},"
                  f"lowest_cell_z={min_z}")
            # 2nd: check eligiblity
            for cell in cell_list:
                # init variables
                floor_num = int(floor.split("_")[1])
                cell_pos = cell.split("_")[1:]
                cell_x = int(cell_pos[0])
                cell_z = int(cell_pos[2])

                if cell_x == max_x:
                    self.build_wall(floor_num, (cell_x, cell_z), "+x")
                elif cell_x == min_x:
                    self.build_wall(floor_num, (cell_x, cell_z), "-x")
                if cell_z == max_z:
                    self.build_wall(floor_num, (cell_x, cell_z), "+z")
                elif cell_z == min_z:
                    self.build_wall(floor_num, (cell_x, cell_z), "-z")

                if floor_num == self.building_height:
                    if cell_x == max_x or cell_x == min_x:
                        if cell_z != max_z and cell_z != min_z:
                            self.build_roof((cell_x, cell_z),
                                            (min_x, max_x), "x")
                    if cell_z == max_z or cell_z == min_z:
                        if cell_x != max_x and cell_x != min_x:
                            self.build_roof((cell_x, cell_z),
                                            (min_z, max_z), "z")

                cmds.delete(cell)

            corners = ("+x+z", "+x-z", "-x+z", "-x-z")
            for corner in corners:
                if corner[0] == "+":
                    x = max_x
                else:
                    x = min_x
                if corner[2] == "+":
                    z = max_z
                else:
                    z = min_z
                self.build_column(floor_num, (x, z), corner)
                self.build_band_corner(floor_num, (x, z), corner)
                if floor_num == self.building_height:
                    self.build_roof_corner((x, z), corner)

        cmds.parent("roof_grp", "SM_ApartmentBuilding")

        cmds.xform("SM_ApartmentBuilding",
                   scale=(self.master_scale,
                          self.master_scale,
                          self.master_scale))

    def build_wall(self, floor_num, pos, dir):

        self.build_window(floor_num, pos, dir)
        self.build_band(floor_num, pos, dir)
        self.build_balcony(floor_num, pos, dir)
        self.build_awning(floor_num, pos, dir)

    def build_window(self, floor_num, pos, dir):
        floor_height = (floor_num-1)*self.cell_height+.5*self.cell_height
        degrees_per_direction = {"+x": 90, "-x": -90, "+z": 0, "-z": 180}
        rotation = degrees_per_direction[dir]
        axis = dir[1]
        polarity = int(dir[0]+"1")

        window_obj_name = cmds.polyPlane(  # create window
            h=self.cell_height,
            w=self.cell_width,
            subdivisionsX=1,
            subdivisionsY=1,
            name=f"window_{pos}_{dir}")[0]
        cmds.rotate(90, 0, 0)  # stand upright
        cmds.rotate(0, rotation, 0, relative=True)  # face correct direction
        cmds.move(  # move to cell center
            (pos[0]-1)*self.cell_width,
            floor_height,
            (pos[1]-1)*self.cell_width)
        if axis == "x":  # move to edge of cell
            cmds.move(polarity * .5 * self.cell_width, 0, 0,
                      relative=True)
        elif axis == "z":
            cmds.move(0, 0, polarity * .5 * self.cell_width,
                      relative=True)

        cmds.parent(window_obj_name, f"floor_{floor_num}")

    def build_column(self, floor_num, pos, dir):
        floor_height = (floor_num-1)*self.cell_height+.5*self.cell_height
        polarity_x = int(dir[0]+"1")
        polarity_z = int(dir[2]+"1")
        column_obj_name = cmds.polyCube(  # create column
            h=self.cell_height,
            w=60,
            d=60,
            name=f"column_{pos}_{dir}")[0]
        cmds.move(  # move to cell center
            (pos[0]-1)*self.cell_width,
            floor_height,
            (pos[1]-1)*self.cell_width)
        cmds.move(  # move to the corner
                  polarity_x * .5 * self.cell_width,
                  0,
                  polarity_z * .5 * self.cell_width,
                  relative=True)
        cmds.parent(column_obj_name, f"floor_{floor_num}")

    def build_band_corner(self, floor_num, pos, dir):
        if floor_num == self.building_height:
            overhang = self.cornice_overhang
            height = self.cornice_height
            name = "cornice"
        else:
            overhang = self.midline_overhang
            height = self.midline_height
            name = "midline"

        polarity_x = int(dir[0]+"1")
        polarity_z = int(dir[2]+"1")

        band_corner_obj_name = cmds.polyCube(  # create cornice corner
            h=height,
            w=overhang,
            d=overhang,
            name=f"{name}_corner_{pos}")[0]
        cmds.move(  # move to cell center
            (pos[0]-1)*self.cell_width,
            floor_num*self.cell_height+.5*height,
            (pos[1]-1)*self.cell_width)
        cmds.move(  # move to the corner
                polarity_x * (.5 * self.cell_width + .5 * overhang),
                0,
                polarity_z * (.5 * self.cell_width + .5 * overhang),
                relative=True)
        cmds.parent(band_corner_obj_name, f"floor_{floor_num}")

    def build_band(self, floor_num, pos, dir):
        degrees_per_direction = {"+x": 90, "-x": -90, "+z": 0, "-z": 180}
        rotation = degrees_per_direction[dir]
        axis = dir[1]
        polarity = int(dir[0]+"1")

        if floor_num == self.building_height:
            height = self.cornice_height
            overhang = self.cornice_overhang
            name = "cornice"
        else:
            height = self.midline_height
            overhang = self.midline_overhang
            name = "midline"

        band_obj_name = cmds.polyCube( # create band
            d=overhang,
            w=self.cell_width,
            h=height,
            name=f"{name}_{pos}"
        )[0]
        cmds.move(  # move to cell center
            (pos[0]-1)*self.cell_width,
            floor_num*self.cell_height+.5*height,
            (pos[1]-1)*self.cell_width)
        if axis == "x":  # move to edge of cell
            cmds.rotate(0, rotation, 0, relative=True, objectSpace=True)
            cmds.move(polarity*(.5*self.cell_width+.5*overhang), 0, 0,
                      relative=True)
        elif axis == "z":
            cmds.move(0, 0, polarity*(.5*self.cell_width+.5*overhang),
                      relative=True)

        cmds.parent(band_obj_name, f"floor_{floor_num}")

    def build_balcony(self, floor_num, pos, dir):
        pass

    def build_awning(self, floor_num, pos, dir):
        pass

    def build_roof_corner(self, pos, dir):
        height = self.roof_height
        width = self.roof_depth
        difference = .5*(width-self.cell_width)

        polarity_x = int(dir[0]+"1")
        polarity_z = int(dir[2]+"1")

        roof_corner_obj_name = cmds.polyCube(  # create geo
            w=width,
            d=width,
            h=height,
            name=f"rooftop_corner_{pos}_{dir}"
        )
        cmds.move(  # move to pos
            (polarity_x*(pos[0]-1)*self.cell_width),
            .5*height+self.building_height*self.cell_height+self.cornice_height,
            (polarity_z*(pos[1]-1)*self.cell_width)
        )
        cmds.move(  # push toward corner
            polarity_x*difference,
            0,
            polarity_z*difference,
            relative=True,
            objectSpace=True
        )

        cmds.parent(roof_corner_obj_name, "roof_grp")

    def build_roof(self, pos, range_along_axis, axis):
        if axis == "x":
            pos_on_axis = pos[0]
        else:
            pos_on_axis = pos[1]
        if pos_on_axis == range_along_axis[0]:
            polarity = -1
        else:
            polarity = 1

        roof_obj_name = cmds.polyCube(  # create geo
            d=self.roof_depth,
            w=self.cell_width,
            h=self.roof_height,
            name=f"roof_{pos}"
        )[0]
        cmds.move(  # move to pos
            (pos[0]-1)*self.cell_width,
            .5*self.roof_height+self.building_height*self.cell_height+self.cornice_height,
            (pos[1]-1)*self.cell_width
        )
        if axis == "x":
            cmds.move(  # push outward, rotate
                    polarity*20,
                    0,
                    0,
                    relative=True, objectSpace=True)
            cmds.rotate(0, 90, 0, relative=True, objectSpace=True)
        else:
            cmds.move(  # push outward
                    0,
                    0,
                    polarity*20,
                    relative=True, objectSpace=True)

        cmds.parent(roof_obj_name, "roof_grp")
