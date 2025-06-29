
import re
from typing import Any
import uuid

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_AllplanSettings as AllplanSettings

from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementListService import BuildingElementListService
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementParameterListUtil import BuildingElementParameterListUtil
from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from ControlPropertiesUtil import ControlPropertiesUtil
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from InputMode import InputMode
from StringTableService import StringTableService

from BuildingElementPaletteService import BuildingElementPaletteService
from BaseInteractor import BaseInteractor, BaseInteractorData

from .Utility import Utility as Utility
from .Utility.Properties import CriticalZoneType


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version
    Args:
        build_ele: the building element.
        version:   the current Allplan version
    Returns:
        True/False if version is supported by this script
    """

    del build_ele
    del version

    return True

def create_interactor(interactor_data: BaseInteractorData):

    return CriticalZone(interactor_data)


class CriticalZone(BaseInteractor):
    def __init__(self, interactor_data: BaseInteractorData):
        self.build_ele = interactor_data.build_ele_list[0]
        self.palette_service = BuildingElementPaletteService(interactor_data.build_ele_list,
                                                         interactor_data.build_ele_composite,
                                                         self.build_ele.script_name,
                                                         interactor_data.control_props_list,
                                                         self.build_ele.pyp_file_name)
        self.coord_input = interactor_data.coord_input

        self.pyp_path = interactor_data.pyp_path
        self.str_table_service = interactor_data.global_str_table_service
        self.modify_uuid_list = interactor_data.modify_uuid_list
        self.control_props_list  = interactor_data.control_props_list
        self.build_ele_list = interactor_data.build_ele_list
        self.build_ele_list[0].UUID_STRING.value  = str(uuid.uuid4())
        self.build_ele = self.build_ele_list[0]
        self.doc = self.coord_input.GetInputViewDocument()

        # Get string table
        self.str_table = self.build_ele.get_string_tables()[0]

        self.ctrl_prop_util = ControlPropertiesUtil(self.control_props_list, self.build_ele_list)
        self.post_element_selection = AllplanIFW.PostElementSelection()

        # Attribute of slab and column
        self.column_selected = False
        self.slab_selected = False
        # self.wall_selected = False

        self.column = None
        self.slab = None
        self.selected_walls = []
        self.wall_end = None
        self.wall_straight = None

        self.selected_success = False


        self.element_filter_column, self.element_filter_slab, self.element_filter_wall = Utility.get_filters_selection()

        self.palette_service.show_palette(self.build_ele.pyp_file_name)


    def on_value_input_control_enter(self) -> bool:
        return True

    def on_control_event(self, _event_id) -> None:
        """
        On control event
        Args:
            _event_id: event id of control.
        """

        pass

    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """
        pass

    def modify_element_property(self, page: int, name: str, value: Any):
        """To modify property of element on palette
        """
        self.palette_service.modify_element_property(page, name, value)
        self.palette_service.update_palette(-1, False)

        return True

    def process_mouse_msg(self,
                          mouse_msg,
                          pnt,
                          msg_info) -> bool:
        """ Handles the process mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        if not self.slab_selected:
            self.slab_mouse(mouse_msg, pnt, msg_info)
            return True

        if self.build_ele.CriticalZoneType.value == CriticalZoneType.Column.value:

            if not self.column_selected :
                self.column_mouse(mouse_msg, pnt, msg_info)
                print("Column: ", self.column)
                return True
        elif self.build_ele.CriticalZoneType.value == CriticalZoneType.WallCorner.value:
            if not self.selected_walls :
                self.selection_wall_erea('Select wall corner area')
                self.selected_walls = list(self.post_element_selection.GetSelectedElements(self.doc))
                print("Walls: ", self.selected_walls)
                return True
        else:
            if not self.wall_end:
                self.wall_end_mouse(mouse_msg, pnt, msg_info)
                return True

            if self.wall_end and not self.wall_straight:
                self.wall_straight_mouse(mouse_msg, pnt, msg_info)
                return True

            if  self.wall_straight and self.wall_end:
                geo_wall_end = self.wall_end.GetPureArchitectureElementGeometry()
                geo_wall_straight = self.wall_straight.GetPureArchitectureElementGeometry()
                result, brep_intersection = AllplanGeo.MakeIntersection(geo_wall_end, geo_wall_straight)
                # result, brep_intersection = AllplanGeo.Intersect(geo_wall_end, geo_wall_straight)
                check_intersection = brep_intersection.IsValid()
                print(result, brep_intersection)
                if not result:
                    AllplanUtil.ShowMessageBox(
                        'The wall end and wall straight are not intersected, please select again',
                        AllplanUtil.MB_OK
                    )
                    self.wall_end = None
                    self.wall_straight = None
                    return True
                AllplanUtil.ShowMessageBox('Fish select wall end', AllplanUtil.MB_OK)
                # self.selected_success = True
                return False



        return True

    def on_preview_draw(self):
        """
        Handles the preview draw event
        """
        pass
    def draw_preview(self):
        """ Draw the preview of imported skp model
        """
        pass

    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()
        return True

    def column_mouse(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event for column only

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True, self.element_filter_column)
        if self.coord_input.IsMouseMove(mouse_msg):
            return False

        self.column = self.coord_input.GetSelectedElement()
        self.column_selected = True

        return True

    def slab_mouse(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event for column only

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True, self.element_filter_slab)
        if self.coord_input.IsMouseMove(mouse_msg):
            return False

        self.slab = self.coord_input.GetSelectedElement()
        self.ctrl_prop_util.set_enable_condition("CriticalZoneType", "False")

        self.palette_service.update_palette(-1, True)
        self.slab_selected = True

        return True

    def selection_wall_erea(self, display_text: str):
        """Turn on area selection mode

            Args:
                display_text (str): message for dialog line

        """
        self.post_element_selection = AllplanIFW.PostElementSelection()
        AllplanIFW.InputFunctionStarter.StartElementSelect(
            display_text,
            self.element_filter_wall,
            self.post_element_selection, True,
            AllplanIFW.SelectionMode.eSelectSubObject
        )

    def wall_end_mouse(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event for column only

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True, self.element_filter_wall)
        if self.coord_input.IsMouseMove(mouse_msg):
            return False

        self.wall_end = self.coord_input.GetSelectedElement() if not self.coord_input.GetSelectedElement().IsNull() else None

        return True

    def wall_straight_mouse(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event for column only

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True, self.element_filter_wall)
        if self.coord_input.IsMouseMove(mouse_msg):
            return False

        self.wall_straight = self.coord_input.GetSelectedElement() if not self.coord_input.GetSelectedElement().IsNull() else None

        return True

