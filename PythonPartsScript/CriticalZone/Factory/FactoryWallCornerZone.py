from .BaseFactoryZone import BaseFactoryZone
from ..Geometry.Slab import Slab
from ..Geometry.WallCorner import WallCorner

import NemAll_Python_Geometry as AllplanGeo


class FactoryWallCornerZone(BaseFactoryZone):

    @staticmethod
    def create_zone(slab: Slab, element_connect: WallCorner) -> AllplanGeo.BRep3D:
        """Factory method to create a WallCornerZone instance.
        Args:
            slab: The slab associated with the wall corner zone.
            element_connect: The connection elements for the wall corner zone.
        Returns:
            A new instance of WallCornerZone.
        """
        return AllplanGeo.BRep3D()