"""
Module for basic geometrical data
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


class ComponentGeometry:
    """ A class for storing geometry data of an aircraft component """

    def __init__(self):
        self.reference_length = None
        """ Reference length of the element """

        self.reference_area = None
        """ Reference area of the element """

        self.wetted_area = None
        """ Area of wetted surface of the element """

        self.mean_relative_thickness = None
        """ Mean value of thickness/chord ratio of the element """

        self.sweep_25 = None
        """ Sweep value at 25% chord of the element """
