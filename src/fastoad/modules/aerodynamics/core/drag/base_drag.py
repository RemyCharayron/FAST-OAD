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
from typing import TypeVar, Union

import numpy as np

from fastoad.modules.aerodynamics.core.drag.drag_functions import get_turbulent_friction_drag
from fastoad.modules.aerodynamics.core.geometry.base_geometry import ComponentGeometry
from fastoad.utils.physics import Atmosphere

Geometry = TypeVar('Geometry', bound=ComponentGeometry)


class AbstractDrag(ABC):
    """
    Class for drag computation

    :param geometry: instance that contains geometrical information
    :param reference_area:
    """

    def __init__(self, geometry: Geometry, reference_area: float):
        self._geometry: Geometry = geometry
        self._reference_area: float = reference_area

    @abstractmethod
    def get_zero_lift_drag_coefficient(self,
                                       mach: Union[float, np.ndarray],
                                       altitude: Union[float, np.ndarray]) \
            -> Union[float, np.ndarray]:
        """
        Computes drag coefficient at lift=0 (also called parasitic drag by opposition to lift-induced
        drag).

        If mach and altitude are both arrays, they are expected to have same shape.
        Then output will have same shape as input array(s).

        :param mach: Mach number
        :param altitude: Altitude in meters
        :return: drag coefficient with respect to reference_area specified at initialization
        """

    def get_lift_induced_drag_coefficient(self,
                                          lift_coefficient: Union[float, np.ndarray],
                                          mach: Union[float, np.ndarray]) \
            -> Union[float, np.ndarray]:
        """
        Computes drag coefficient that is due to lift.

        If mach and lift_coefficient are both arrays, they are expected to have same shape.
        Then output will have same shape as input array(s).

        :param lift_coefficient:
        :param mach:
        :return:
        """
        pass

    def get_friction_drag_coefficient(self,
                                      mach: Union[float, np.ndarray],
                                      altitude: Union[float, np.ndarray]) \
            -> Union[float, np.ndarray]:
        """
        Computes friction drag coefficient.

        :param mach: Mach number
        :param altitude: Altitude in meters
        :return: drag coefficient with respect to reference_area specified at initialization
        """
        reynolds = Atmosphere(altitude).get_unitary_reynolds(mach)
        cf = get_turbulent_friction_drag(reynolds, mach)

        # get coefficient with respect to provided reference area
        return cf * self._geometry.wetted_area / self._reference_area
