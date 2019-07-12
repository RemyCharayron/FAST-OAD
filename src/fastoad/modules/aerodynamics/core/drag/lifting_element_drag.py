"""
Module for drag from wing and horizontal and vertical tails
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

from abc import ABC, abstractmethod

import numpy as np

from fastoad.modules.aerodynamics.core.drag.base_drag import AbstractDrag

K_I = 0.04
""" Wing/fuselage interaction coefficient """


class LiftingElementDrag(AbstractDrag, ABC):
    """

    From Supaero course "Avant-projet d'un avion de transport commercial"

    .. math::
        Cd_0 = ( (K_t + K_c)K_{\\phi} + K_i + 1) * Cd_f

        Cd_i =

    """

    def get_zero_lift_drag_coefficient(self, mach, altitude):
        cf = self.get_friction_drag_coefficient(mach, altitude)
        kt = self.get_toc_factor()
        kc = self.get_camber_factor()
        ks = self.get_sweep_factor()
        ki = self.get_interaction_factor()
        return ((kt + kc) * ks + ki + 1) * cf

    def get_toc_factor(self):
        """ Thickness factor """
        toc = self._geometry.mean_relative_thickness
        return 4.688 * toc ** 2 + 3.146 * toc

    def get_sweep_factor(self):
        """ Wing sweep factor """
        sweep_25 = self._geometry.sweep_25  # in degrees
        return 1 - 0.000178 * sweep_25 ** 2 - 0.0065 * sweep_25

    @abstractmethod
    def get_camber_factor(self, lift_coefficient=0):
        """ Camber factor. Depends on lift"""
        pass

    @abstractmethod
    def get_interaction_factor(self):
        pass


class HorizontalTailDrag(LiftingElementDrag):

    def get_camber_factor(self):
        return 0.

    def get_interaction_factor(self):
        return K_I / 4.


class VerticalTailDrag(LiftingElementDrag):

    def get_camber_factor(self):
        return 0.

    def get_interaction_factor(self):
        return K_I / 8.


class WingDrag(LiftingElementDrag):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cl = 0.

    def set_lift_coefficient(self, cl):
        self._cl = cl

    def get_camber_factor(self):
        sweep_25 = np.radians(self._geometry.sweep_25)
        unswept_cl = self._cl / (np.cos(sweep_25) ^ 2)
        return 2.859 * unswept_cl ^ 3 - 1.849 * unswept_cl ^ 2 + 0.382 * unswept_cl + 0.06

    def get_interaction_factor(self):
        return K_I
