import math

from typing import Dict, List, Optional, Set, Union

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW


def get_filters_selection():
    '''
        Get_filters_selection
    '''
    #----------------------- column
    type_query_column = AllplanIFW.QueryTypeID(AllplanElementAdapter.Column_TypeUUID)
    sel_query_column = AllplanIFW.SelectionQuery(type_query_column)
    element_filter_column = AllplanIFW.ElementSelectFilterSetting(sel_query_column, True)

    #----------------------- slab
    type_query_slab = [AllplanIFW.QueryTypeID(AllplanElementAdapter.Slab_TypeUUID),
                       AllplanIFW.QueryTypeID(AllplanElementAdapter.Volume3D_TypeUUID)]
    sel_query_slab = AllplanIFW.SelectionQuery(type_query_slab)
    element_filter_slab = AllplanIFW.ElementSelectFilterSetting(sel_query_slab, True)

    #----------------------- wall
    sel_query_wall = AllplanIFW.SelectionQuery([
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallAxisArc_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallAxisChain_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallAxisClothoid_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallAxisLine_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallAxisPolyline_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallAxisSpline_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallAxis_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallInfraction_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.WallTier_TypeUUID),
        AllplanIFW.QueryTypeID(AllplanElementAdapter.Wall_TypeUUID)
    ])
    element_filter_wall = AllplanIFW.ElementSelectFilterSetting(sel_query_wall, True)
    return element_filter_column, element_filter_slab, element_filter_wall