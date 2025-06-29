from .BaseFactoryZone import BaseFactoryZone
from ..Geometry.Slab import Slab
from ..Geometry.Wall import Wall

import NemAll_Python_Geometry as AllplanGeo

class FactoryWallEndZone(BaseFactoryZone):

    @staticmethod
    def create_zone(slab: Slab,element_connect: Wall) -> AllplanGeo.BRep3D:
        """        Factory method to create a WallEndZone instance.
        Args:
            slab: The slab associated with the wall end zone.
            element_connect: The connection elements for the wall end zone.
        Returns:
            A new instance of WallEndZone.
        """
        return AllplanGeo.BRep3D()
