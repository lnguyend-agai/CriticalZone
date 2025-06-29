import math
from functools import partial
from typing import Dict, List, Optional, Set, Union

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW
from Utilities.AttributeIdEnums import AttributeIdEnums
from PythonPartTransaction import PythonPartTransaction
from BuildingElementAttributeList import BuildingElementAttributeList
from PythonPartUtil import PythonPartUtil



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

def get_element_attributes(element: AllplanElementAdapter.BaseElementAdapter):
    """get element's attributes

    Args:
        element (BaseElementAdapter): element

    Returns:
        dictionary: dictionary {attribute_id: value}
    """
    attributes = AllplanBaseElements.ElementsAttributeService.GetAttributes(element, AllplanBaseElements.eAttibuteReadState.ReadAllAndComputable)
    attributes_dict = {}
    for attribute in attributes:
        if attribute[1] != None:
            attributes_dict.setdefault(attribute[0], attribute[1])

    return attributes_dict

def get_dimension(element: AllplanElementAdapter.BaseElementAdapter, is_open: bool = False):
    """Get dimension attributes of wall, opening"""
    if not element:
        return dict()
    attributes_dict = get_element_attributes(element)

    dimensions = {
        "width": attributes_dict[AttributeIdEnums.THICKNESS.value] * 1000 if is_open else attributes_dict[AttributeIdEnums.THICKNESS.value] * 1000,
        "length": attributes_dict[AttributeIdEnums.LENGTH.value] * 1000 if is_open else max(attributes_dict[AttributeIdEnums.LENGTH.value] * 1000, 0.5 * (attributes_dict[AttributeIdEnums.PERIMETER.value] - 2 * attributes_dict[AttributeIdEnums.THICKNESS.value] * 1000)),
        "height": attributes_dict[AttributeIdEnums.HEIGHT.value] * 1000,
        "volume": attributes_dict[AttributeIdEnums.VOLUME.value],
        "net_volume": attributes_dict[AttributeIdEnums.NET_VOLUME.value] * 10**9 if AttributeIdEnums.NET_VOLUME.value in attributes_dict else attributes_dict[AttributeIdEnums.VOLUME.value]
    }
    return dimensions

def get_8_points(point_list, delta_z=None):
    bottom_list: List[AllplanGeo.Point3D] = get_4_bottom_points(point_list)

    if round(bottom_list[0].Y, 2) >= round(bottom_list[3].Y, 2):
        bottom_list = [bottom_list[3], bottom_list[2],
                       bottom_list[1], bottom_list[0]]
    if not delta_z:
        delta_z = get_delta_z(point_list)
    return bottom_list + [point + AllplanGeo.Point3D(0, 0, delta_z) for point in bottom_list]

def get_4_bottom_points(point_list_origin):
    # for case 8 points
    if not point_list_origin:
        print("Point list is empty, can't get 4 bottom points")
        return []
    # Get only min z from list
    point_list = get_points_min_z(point_list_origin)

    # if len(point_list) != 4: raise Exception("get_4_bottom_points fail")

    # First point is min y point
    first_pnt = get_first_point(point_list)

    max_distance = get_max_distance(first_pnt, point_list)
    min_distance = get_min_distance(first_pnt, point_list)

    third_pnt = None
    fourth_pnt = None
    second_pnt = None
    for point in point_list:
        if abs(first_pnt.GetDistance(point)) == max_distance and not third_pnt:
            third_pnt = point
        elif abs(first_pnt.GetDistance(point)) == min_distance and not fourth_pnt:
            fourth_pnt = point
        elif abs(first_pnt.GetDistance(point)) != 0 and not second_pnt:
            second_pnt = point

    return [first_pnt, second_pnt, third_pnt, fourth_pnt]

def get_min_distance(point, point_list):
    return min([abs(point.GetDistance(ref_point)) for ref_point in point_list
                if abs(point.GetDistance(ref_point)) != 0])

def get_max_distance(point, point_list):
    return max([abs(point.GetDistance(ref_point)) for ref_point in point_list])

def get_min_x(point_list):
    return min([point.X for point in point_list])

def get_max_x(point_list):
    return max([point.X for point in point_list])

def get_min_y(point_list):
    return min([point.Y for point in point_list])

def get_max_y(point_list):
    return max([point.Y for point in point_list])

def get_min_z(point_list):
    return min([point.Z for point in point_list])

def get_max_z(point_list):
    return max([point.Z for point in point_list])

def get_delta_z(point_list):
    return abs(get_max_z(point_list) - get_min_z(point_list))

def get_points_min_z(point_list: List[AllplanGeo.Point3D]):
    if not point_list:
        print("Point list is empty, can't get point min z")
        return []
    z_min = get_min_z(point_list)
    return [point for point in point_list if round(point.Z, 0) == round(z_min, 0)]

def get_points_max_z(point_list: List[AllplanGeo.Point3D]):
    if not point_list:
        print("Point list is empty, can't get point max z")
        return []
    z_max = get_max_z(point_list)
    return [point for point in point_list if round(point.Z, 0) == round(z_max, 0)]

def get_first_point(point_list: Union[List[AllplanGeo.Point3D], List[AllplanGeo.Point2D]]):
    """Get the point has x min.
       if more than 2 points satisfy the condition, get the the point with lowest y

    Args:
        point_list (list[Point3D | Point2D]):

    Returns:
        Point3D | Point2D | None:
    """
    if not point_list:
        print("Point list is empty, can't get first point")
        return None
    x_min = get_min_x(point_list)
    first_pnt_list = [point for point in point_list if round(point.X, 0) == round(x_min, 0)]
    if len(first_pnt_list) == 1:
        return first_pnt_list[0]
    else:
        y_min = get_min_y(first_pnt_list)
        return [point for point in first_pnt_list if round(point.Y, 0) == round(y_min, 0)][0]

def round_list_point_3d(list_point: List[AllplanGeo.Point3D]) -> List[AllplanGeo.Point3D]:

    return list(map(partial(round_point_3d, ndigits=2), list_point))

def round_point_3d(point: AllplanGeo.Point3D, ndigits: int=0):
    if type(point) is AllplanGeo.Point3D:
        return AllplanGeo.Point3D(round(point.X, ndigits),
                                  round(point.Y, ndigits),
                                  round(point.Z, ndigits))

    raise TypeError("Only Point3D")


def create_pythonpart_util(bounding_box=None, color: int = 23, layer=3707) -> PythonPartUtil:

    """ Create the PythonPartUtil """
    # ----------------- create python part util
    pyp_util = PythonPartUtil()


    # ----------------- collect the common properties
    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.Color = color
    com_prop.Layer = layer
    com_prop.HelpConstruction = True

    # ----------------- add view to python part
    view_box = AllplanBasisElements.ModelElement3D(com_prop, bounding_box)
    pyp_util.add_pythonpart_view_2d3d(view_box)

    # ----------------- add attributes to python part
    attr_list = [
        AllplanBaseElements.AttributeString(AttributeIdEnums.NAME.value, "CriticalZone"),
    ]
    build_ele_attr_list = BuildingElementAttributeList()
    build_ele_attr_list.add_attribute_list(attr_list)
    pyp_util.add_attribute_list(build_ele_attr_list)

    return pyp_util

def create_pythonpart_wall(
    doc,
    placement_matrix: AllplanGeo.Matrix3D,
    view_projection,
    build_ele_list,
    modify_uuid_list: List,
    pp_util: PythonPartUtil,
    uuid_parameter_name = "PythonPartUUID",
    auto_update_mark: bool = False,
    type_display_name = 'PythonPart',
    connect_to_elements = None):

    """ Create the PythonPart """

    if connect_to_elements != None:
        pyp_transaction = PythonPartTransaction(doc, connect_to_ele = connect_to_elements)
    else:
        pyp_transaction = PythonPartTransaction(doc)
    pyp_transaction.execute(placement_matrix,
                            view_projection,
                            pp_util.create_pythonpart(build_ele_list, type_display_name = type_display_name),
                            modify_uuid_list,
                            rearrange_reinf_pos_nr=False,
                            append_reinf_pos_nr=auto_update_mark,
                            uuid_parameter_name=uuid_parameter_name,
                            use_system_angle = False,
                            )