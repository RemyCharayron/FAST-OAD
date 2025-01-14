"""
    FAST - Copyright (c) 2016 ONERA ISAE
"""
#  This file is part of FAST-OAD : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2021 ONERA & ISAE-SUPAERO
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
from openmdao.core.explicitcomponent import ExplicitComponent


class Cd0Total(ExplicitComponent):
    def initialize(self):
        self.options.declare("low_speed_aero", default=False, types=bool)

    def setup(self):
        self.low_speed_aero = self.options["low_speed_aero"]

        self.add_input("data:geometry:aircraft:wetted_area", val=np.nan, units="m**2")

        if self.low_speed_aero:
            self.add_input("data:aerodynamics:wing:low_speed:CD0", shape_by_conn=True, val=np.nan)
            self.add_input(
                "data:aerodynamics:fuselage:low_speed:CD0", shape_by_conn=True, val=np.nan
            )
            self.add_input("data:aerodynamics:horizontal_tail:low_speed:CD0", val=np.nan)
            self.add_input("data:aerodynamics:vertical_tail:low_speed:CD0", val=np.nan)
            self.add_input("data:aerodynamics:nacelles:low_speed:CD0", val=np.nan)
            self.add_input("data:aerodynamics:pylons:low_speed:CD0", val=np.nan)
            self.add_output(
                "data:aerodynamics:aircraft:low_speed:CD0",
                copy_shape="data:aerodynamics:wing:low_speed:CD0",
            )
        else:
            self.add_input("data:aerodynamics:wing:cruise:CD0", shape_by_conn=True, val=np.nan)
            self.add_input("data:aerodynamics:fuselage:cruise:CD0", shape_by_conn=True, val=np.nan)
            self.add_input("data:aerodynamics:horizontal_tail:cruise:CD0", val=np.nan)
            self.add_input("data:aerodynamics:vertical_tail:cruise:CD0", val=np.nan)
            self.add_input("data:aerodynamics:nacelles:cruise:CD0", val=np.nan)
            self.add_input("data:aerodynamics:pylons:cruise:CD0", val=np.nan)
            self.add_output(
                "data:aerodynamics:aircraft:cruise:CD0",
                copy_shape="data:aerodynamics:wing:cruise:CD0",
            )

    def setup_partials(self):
        self.declare_partials("*", "*", method="fd")

    def compute(self, inputs, outputs):
        wet_area_total = inputs["data:geometry:aircraft:wetted_area"]
        if self.low_speed_aero:
            cd0_wing = inputs["data:aerodynamics:wing:low_speed:CD0"]
            cd0_fus = inputs["data:aerodynamics:fuselage:low_speed:CD0"]
            cd0_ht = inputs["data:aerodynamics:horizontal_tail:low_speed:CD0"]
            cd0_vt = inputs["data:aerodynamics:vertical_tail:low_speed:CD0"]
            cd0_nac = inputs["data:aerodynamics:nacelles:low_speed:CD0"]
            cd0_pylon = inputs["data:aerodynamics:pylons:low_speed:CD0"]
        else:
            cd0_wing = inputs["data:aerodynamics:wing:cruise:CD0"]
            cd0_fus = inputs["data:aerodynamics:fuselage:cruise:CD0"]
            cd0_ht = inputs["data:aerodynamics:horizontal_tail:cruise:CD0"]
            cd0_vt = inputs["data:aerodynamics:vertical_tail:cruise:CD0"]
            cd0_nac = inputs["data:aerodynamics:nacelles:cruise:CD0"]
            cd0_pylon = inputs["data:aerodynamics:pylons:cruise:CD0"]

        k_techno = 1
        k_parasite = (
            -2.39 * pow(10, -12) * wet_area_total ** 3
            + 2.58 * pow(10, -8) * wet_area_total ** 2
            - 0.89 * pow(10, -4) * wet_area_total
            + 0.163
        )

        cd0_total_hs = cd0_wing + cd0_fus + cd0_ht + cd0_vt + cd0_nac + cd0_pylon
        cd0_total = cd0_total_hs * (1.0 + k_parasite * k_techno)

        if self.low_speed_aero:
            outputs["data:aerodynamics:aircraft:low_speed:CD0"] = cd0_total
        else:
            outputs["data:aerodynamics:aircraft:cruise:CD0"] = cd0_total
