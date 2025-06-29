
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
from Utility import Utility

class BaseElement:
    """
    Base class for all elements in the Critical Zone module.
    This class provides a common interface and basic functionality for all derived element classes.
    """

    def __init__(self, element_adapter: AllplanElementAdapter.BaseElementAdapter):
        """
        Initializes the BaseElement with interactor data.

        Args:
            interactor_data: Data required for the interactor, including services and properties.
        """
        self.element_adapter = element_adapter
        self.type_id = element_adapter.GetElementAdapterType().GetGuid()
        self.unique_id = element_adapter.GetModelElementUUID()
        self.geometry_pure = Utility.round_list_point_3d(
            Utility.get_8_points(
                list(self.element_adapter.GetPureArchitectureElementGeometry().GetVertices())
            )
        )
        self.geometry = Utility.round_list_point_3d(Utility.get_8_points(self.geometry_pure))


class Cube(BaseElement):
    """
    Represents a cube element in the Critical Zone module.
    Inherits from BaseElement and implements specific functionality for cube elements.
    """

    def __init__(self, element_adapter: AllplanElementAdapter.BaseElementAdapter):
        """
        Initializes the Cube element with specific properties and services.
        """
        super().__init__(element_adapter)
        # Initialize cube-specific properties here
        self.element_attributes = Utility.get_dimension(self.element_adapter)
        self.length = self.element_attributes["length"]
        self.height = self.element_attributes["height"]
        self.width = self.element_attributes["width"]
        self.net_volume = self.element_attributes["net_volume"]