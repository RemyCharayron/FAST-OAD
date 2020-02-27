"""
Where initialization operations can be done
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

from pelix.constants import BundleActivator

from fastoad.register import register_openmdao_systems


@BundleActivator
class FASTOADActivator:
    """
    Activator class where internal modules are loaded

    Having the loading operation in start() method ensures it is done only once
    as long as this iPOPO bundle is active.
    """

    def start(self, context):
        """
        Loads inner packages of FAST
        """
        register_openmdao_systems()