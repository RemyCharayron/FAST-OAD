"""
    Estimation of control surfaces center of gravity
"""

#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2019  ONERA/ISAE
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


class ComputeControlSurfacesCG(ExplicitComponent):
    # TODO: Document equations. Cite sources
    """ Control surfaces center of gravity estimation """

    def setup(self):

        self.add_input('geometry:wing_l0', val=np.nan, units='m')
        self.add_input('geometry:wing_x0', val=np.nan, units='m')
        self.add_input('geometry:wing_y0', val=np.nan, units='m')
        self.add_input('geometry:wing_l2', val=np.nan, units='m')
        self.add_input('geometry:wing_l3', val=np.nan, units='m')
        self.add_input('geometry:wing_y2', val=np.nan, units='m')
        self.add_input('geometry:wing_x3', val=np.nan, units='m')
        self.add_input('geometry:wing_y3', val=np.nan, units='m')
        self.add_input('geometry:wing_position', val=np.nan, units='m')

        self.add_output('cg_airframe:A4', units='m')

        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
        l0_wing = inputs['geometry:wing_l0']
        x0_wing = inputs['geometry:wing_x0']
        y0_wing = inputs['geometry:wing_y0']
        l2_wing = inputs['geometry:wing_l2']
        l3_wing = inputs['geometry:wing_l3']
        y2_wing = inputs['geometry:wing_y2']
        x3_wing = inputs['geometry:wing_x3']
        y3_wing = inputs['geometry:wing_y3']
        fa_length = inputs['geometry:wing_position']

        # TODO: build generic functions to estimate the chord, leading edge,
        # trailing edge with respect to span wise position
        x_leading_edge = x3_wing * (y0_wing - y2_wing) / (y3_wing - y2_wing)
        l_cg_control = l2_wing + \
            (y0_wing - y2_wing) / (y3_wing - y2_wing) * (l3_wing - l2_wing)
        x_cg_control = x_leading_edge + l_cg_control
        x_cg_control_absolute = fa_length - \
            0.25 * l0_wing - x0_wing + x_cg_control

        outputs['cg_airframe:A4'] = x_cg_control_absolute