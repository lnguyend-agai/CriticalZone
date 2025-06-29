from typing import Any
from ..Geometry.Slab import Slab

import NemAll_Python_Geometry as AllplanGeo

class BaseFactoryZone:
    @staticmethod
    def create_zone(slab: Slab, element_connect: Any) -> AllplanGeo.BRep3D:
        return AllplanGeo.BRep3D()

    def create_zone_at_corner(self):
        return AllplanGeo.BRep3D()