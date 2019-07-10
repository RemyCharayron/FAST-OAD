"""
Friction drag estimate
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


import math
import numpy as np
from openmdao.core.explicitcomponent import ExplicitComponent


class CdFriction(ExplicitComponent):
    """
    Component for estimating friction drag

    Friction drag coefficient is computed using formula from Raymer [#Raymer]_

    .. math::
        C_f = \\frac{ 0.455}{  (\log_{10}R)^{2.58} (1+0.144M^2)^{0.65} }

    - :math:`R`: Reynolds number
    - :math:`M`: Mach number


    **Reference:**

    .. [#Raymer] Eq 12.27 from Raymer, D.P., "Aircraft Design: A Conceptual Approach", AIAA, Washington, 1989.

    """

    def setup(self):
        self.add_input('reynolds', val=np.nan)
        self.add_input('mach', val=np.nan)
        self.add_output('cd_friction')

    def compute(self, inputs, outputs):
        reynolds = inputs['reynolds']
        mach = inputs['mach']

        cf_ht_hs = 0.455 / ((1 + 0.126 * mach ** 2) * (math.log10(reynolds)) ** 2.58)
        outputs['cd_friction'] = cf_ht_hs
