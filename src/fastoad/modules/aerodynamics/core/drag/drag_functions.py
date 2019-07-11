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


def get_turbulent_friction_drag(reynolds, mach):
    """
    Estimates friction drag coefficient

    Friction drag coefficient is computed using formula for turbulent flow from Raymer [#Raymer]_:

    .. math::
        C_f = \\frac{ 0.455}{  (\\log_{10}R)^{2.58} (1+0.144M^2)^{0.65} }

    - :math:`M`: Mach number
    - :math:`R`: Reynolds number

    *Note: surface roughness is considered negligible*


    **Reference:**

    .. [#Raymer] Eq 12.27 to 12.29 from Raymer, D.P., *Aircraft Design: A Conceptual Approach*
                , AIAA, Washington, 1989.

    :param reynolds: :math:`R`
    :param mach: :math:`M`
    :return: friction drag coefficient
    """

    cf = 0.455 / (np.log10(reynolds)) ** 2.58 / (1 + 0.144 * mach ** 2) ** 0.65
    return cf
