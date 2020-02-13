"""
    FAST - Copyright (c) 2016 ONERA ISAE
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

from fastoad.modules.geometry.cg_components.compute_aero_center import ComputeAeroCenter
from fastoad.modules.geometry.cg_components.compute_static_margin import ComputeStaticMargin
from fastoad.modules.geometry.geom_components.fuselage.compute_fuselage \
    import ComputeFuselageGeometryBasic, ComputeFuselageGeometryCabinSizing
from fastoad.modules.geometry.geom_components.nacelle_pylons.compute_nacelle_pylons import \
    ComputeNacelleAndPylonsGeometry
from fastoad.modules.geometry.geom_components.wing.compute_wing import ComputeWingGeometry
from fastoad.modules.geometry.get_cg import GetCG
from fastoad.modules.options import OpenMdaoOptionDispatcherGroup, ENGINE_LOCATION_OPTION, \
    TAIL_TYPE_OPTION, AIRCRAFT_FAMILY_OPTION, CABIN_SIZING_OPTION


class Geometry(OpenMdaoOptionDispatcherGroup):
    """ Overall geometry model """

    def initialize(self):
        self.options.declare(ENGINE_LOCATION_OPTION, types=float, default=1.0)
        self.options.declare(TAIL_TYPE_OPTION, types=float, default=0.0)
        self.options.declare(AIRCRAFT_FAMILY_OPTION, types=float, default=1.0)
        self.options.declare(CABIN_SIZING_OPTION, types=float, default=1.0)

    def setup(self):

        if self.options[CABIN_SIZING_OPTION] == 1.0:
            self.add_subsystem('compute_fuselage', ComputeFuselageGeometryCabinSizing(),
                               promotes=['*'])
        else:
            self.add_subsystem('compute_fuselage', ComputeFuselageGeometryBasic(),
                               promotes=['*'])

        self.add_subsystem('compute_wing', ComputeWingGeometry(), promotes=['*'])
        self.add_subsystem('compute_engine_nacelle', ComputeNacelleAndPylonsGeometry(),
                           promotes=['*'])
        self.add_subsystem('get_cg', GetCG(), promotes=['*'])
        self.add_subsystem('compute_aero_center', ComputeAeroCenter(), promotes=['*'])
        self.add_subsystem('compute_sm', ComputeStaticMargin(), promotes=['*'])