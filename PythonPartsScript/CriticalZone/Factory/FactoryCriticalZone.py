
from ..Geometry.CriticalZone import CriticalZone
from ..Geometry.Slab import Slab
from ..Utility.Properties import CriticalZoneType
from .FactoryWallEndZone import FactoryWallEndZone
from .FactoryWallCornerZone import FactoryWallCornerZone
from .FactoryRectangleColumnZone import FactoryRectangleColumnZone
from typing import List
from .CreateZone import BaseZone

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo

class FactoryCriticalZone:

    @staticmethod
    def create_critical_zone(slab: Slab,
                             list_zone_component: List[CriticalZone]) -> AllplanGeo.BRep3D:
        """
        Factory method to create a CriticalZone instance.
        Args:
            slab: The slab associated with the critical zone.
            type_zone: The type of the critical zone.
            list_zone_component: The connection elements for the critical zone.
            layer: The layer on which the critical zone is defined.
            hatch_properties: Properties for hatching the critical zone.
            color: Color of the critical zone.
        Returns:
            A new instance of CriticalZone.
        """
        dict_general_zone: dict[CriticalZoneType, type[BaseZone]] = {CriticalZoneType.Column: FactoryRectangleColumnZone,
                                                                     CriticalZoneType.WallEnd: FactoryWallEndZone,
                                                                     CriticalZoneType.WallCorner: FactoryWallCornerZone}

        final_zone = None
        for zone in list_zone_component:
            create_zone_function = dict_general_zone[zone.type_zone]

            if final_zone is None:
                final_zone = create_zone_function.create_zone(slab, zone.element_connect)
            else:
                new_zone = create_zone_function.create_zone(slab, zone.element_connect)

                _, final_zone = AllplanGeo.MakeUnion(final_zone, new_zone)


        if final_zone is None:
            final_zone = AllplanGeo.BRep3D()

        return final_zone
