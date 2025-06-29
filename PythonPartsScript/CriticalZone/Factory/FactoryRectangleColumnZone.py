from .BaseFactoryZone import BaseFactoryZone
from ..Geometry.Slab import Slab
from ..Geometry.Column import RectangleColumn

import NemAll_Python_Geometry as AllplanGeo


class FactoryRectangleColumnZone(BaseFactoryZone):

    @staticmethod
    def create_zone(slab: Slab, element_connect: RectangleColumn) -> AllplanGeo.BRep3D:
        """Factory method to create a RectangleColumnZone instance.
        Args:
            slab: The slab associated with the rectangle column zone.
            element_connect: The connection elements for the rectangle column zone.
        Returns:
            A new instance of RectangleColumnZone.
        """
        return AllplanGeo.BRep3D()