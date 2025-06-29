from ..Geometry.Slab import Slab
from ..Geometry.Column import RectangleColumn
from ..Geometry.Wall import Wall
from ..Geometry.WallCorner import WallCorner
from ..Utility.Properties import CriticalZoneType


class CriticalZone:

    def __init__(self, slab: Slab,
                 type_zone: CriticalZoneType,
                 element_connect: RectangleColumn | Wall | WallCorner,
                 ):
        """
        Initializes the CriticalZone with the given parameters.
        Args:
            slab: The slab associated with the critical zone.
            type_zone: The type of the critical zone.
            element_connect: The connection elements for the critical zone.
            layer: The layer on which the critical zone is defined.
            hatch_properties: Properties for hatching the critical zone.
            color: Color of the critical zone.
        """
        self.slab = slab
        self.type_zone = type_zone
        self.element_connect = element_connect
        # self.layer = layer
        # self.hatch_properties = hatch_properties
        # self.color = color