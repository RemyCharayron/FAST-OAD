"""
Computation of tail areas w.r.t. HQ criteria
"""
#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA/ISAE
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

from fastoad.modules.options import TAIL_TYPE_OPTION, OpenMdaoOptionDispatcherGroup
from .compute_ht_area import ComputeHTArea
from .compute_vt_area import ComputeVTArea


class ComputeTailAreas(OpenMdaoOptionDispatcherGroup):
    """
    Computes areas of vertical and horizontal tail.

    - Horizontal tail area is computed so it can balance pitching moment of
      aircraft at rotation speed.
    - Vertical tail area is computed so aircraft can have the CNbeta in cruise
      conditions
    """

    def initialize(self):
        self.options.declare(TAIL_TYPE_OPTION, types=float, default=0.)

    def setup(self):
        self.add_subsystem('horizontal_tail', ComputeHTArea(), promotes=['*'])
        self.add_subsystem('vertical_tail', ComputeVTArea(), promotes=['*'])
