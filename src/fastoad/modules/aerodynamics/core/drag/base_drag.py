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

from abc import ABC, abstractmethod
from typing import TypeVar

from fastoad.modules.aerodynamics.core.geometry.base_geometry import ComponentGeometry

Geometry = TypeVar('Geometry', bound=ComponentGeometry)


class AbstractDrag(ABC):

    def __init__(self, geometry: Geometry, reference_area: float):
        self._geometry = geometry
        self._reference_area = reference_area

    @abstractmethod
    def get_zero_lift_drag_coefficient(self, mach, altitude):
        pass

    @abstractmethod
    def get_lift_induced_drag_coefficient(self, lift_coefficient):
        pass
