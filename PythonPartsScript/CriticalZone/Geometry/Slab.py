from .BaseElement import Cube
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

class Slab(Cube):
    def __init__(self, element_adapter: AllplanElementAdapter.BaseElementAdapter):
        super().__init__(element_adapter)

        self.slabs = []

class ListSlab:
    def __init__(self):
        self.slabs = []

    def append(self, slab: Slab):
        """Add a slab to the list"""
        self.slabs.append(slab)

    def remove(self, slab: Slab):
        """Remove a slab from the list"""
        if slab in self.slabs:
            self.slabs.remove(slab)

    def get_slab(self, index: int) -> Slab | None:
        """Get slab at specific index"""
        if 0 <= index < len(self.slabs):
            return self.slabs[index]
        return None

    def get_all_slabs(self) -> list:
        """Get all slabs in the list"""
        return self.slabs.copy()

    def clear(self):
        """Clear all slabs from the list"""
        self.slabs.clear()

    def count(self) -> int:
        """Get the number of slabs in the list"""
        return len(self.slabs)

    def is_empty(self) -> bool:
        """Check if the list is empty"""
        return len(self.slabs) == 0

    def contains(self, slab: 'Slab') -> bool:
        """Check if a slab exists in the list"""
        return slab in self.slabs

    def __len__(self):
        """Return the number of slabs"""
        return len(self.slabs)

    def __getitem__(self, index):
        """Allow indexing access to slabs"""
        return self.slabs[index]

    def __iter__(self):
        """Make the list iterable"""
        return iter(self.slabs)

    def find_slab_by_id(self, slab_id: str) -> Slab | None:
        """Find a slab by its ID

        Args:
            slab_id: The ID of the slab to find

        Returns:
            Slab: The slab if found, None otherwise
        """
        for slab in self.slabs:
            if hasattr(slab, 'id') and slab.id == slab_id:
                return slab
        return None

    def contains_slab_by_id(self, slab_id: str) -> bool:
        """Check if a slab with the given ID exists in the list

        Args:
            slab_id: The ID of the slab to check

        Returns:
            bool: True if slab with ID exists, False otherwise
        """
        return self.find_slab_by_id(slab_id) is not None

    def extend(self, other_list: 'ListSlab'):
        """Extend the current list with slabs from another list"""
        self.slabs.extend(other_list.slabs)
