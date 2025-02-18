"""Sellar discipline 2"""
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

import openmdao.api as om


# @RegisterOpenMDAOSystem("module_management_test.sellar.disc2", domain=ModelDomain.GEOMETRY)
# Instead of being registered with the decorator above, this class is registered
# in register_components.py to test this alternate way
class Disc2(om.ExplicitComponent):
    """ An OpenMDAO component to encapsulate Disc2 discipline """

    def initialize(self):
        self.options.declare("answer", 42)

    def setup(self):
        self.add_input("z", val=[5, 2], desc="", units="m**2")  # for testing non-None units
        self.add_input("y1", val=1.0, desc="")

        self.add_output("y2", val=1.0, desc="")

    def setup_partials(self):
        self.declare_partials("*", "*", method="fd")

    # pylint: disable=invalid-name
    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        """
        Evaluates the equation
        y2 = y1**(.5) + z1 + z2
        """

        z1 = inputs["z"][0]
        z2 = inputs["z"][1]
        y1 = inputs["y1"]

        # Note: this may cause some issues. However, y1 is constrained to be
        # above 3.16, so lets just let it converge, and the optimizer will
        # throw it out
        if y1.real < 0.0:
            y1 *= -1

        outputs["y2"] = y1 ** 0.5 + z1 + z2
