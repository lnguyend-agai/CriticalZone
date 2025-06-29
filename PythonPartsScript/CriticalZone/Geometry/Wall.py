from .BaseElement import Cube
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

class Wall(Cube):
    def __init__(self, element_adapter: AllplanElementAdapter.BaseElementAdapter):
        super().__init__(element_adapter)

        self.walls = []

class ListWall:
    def __init__(self):
        self.walls = []

    def append(self, wall: Wall):
        """Add a wall to the list"""
        self.walls.append(wall)

    def remove(self, wall: Wall):
        """Remove a wall from the list"""
        if wall in self.walls:
            self.walls.remove(wall)

    def get_wall(self, index: int) -> Wall | None:
        """Get wall at specific index"""
        if 0 <= index < len(self.walls):
            return self.walls[index]
        return None

    def get_all_walls(self) -> list:
        """Get all walls in the list"""
        return self.walls.copy()

    def clear(self):
        """Clear all walls from the list"""
        self.walls.clear()

    def count(self) -> int:
        """Get the number of walls in the list"""
        return len(self.walls)

    def is_empty(self) -> bool:
        """Check if the list is empty"""
        return len(self.walls) == 0

    def contains(self, wall: Wall) -> bool:
        """Check if a wall exists in the list"""
        return wall in self.walls

    def __len__(self):
        """Return the number of walls"""
        return len(self.walls)

    def __getitem__(self, index):
        """Allow indexing access to walls"""
        return self.walls[index]

    def __iter__(self):
        """Make the list iterable"""
        return iter(self.walls)

    def find_wall_by_id(self, wall_id: str) -> Wall | None:
        """Find a wall by its ID

        Args:
            wall_id: The ID of the wall to find

        Returns:
            Wall: The wall if found, None otherwise
        """
        for wall in self.walls:
            if hasattr(wall, 'id') and wall.id == wall_id:
                return wall
        return None

    def contains_wall_by_id(self, wall_id: str) -> bool:
        """Check if a wall with the given ID exists in the list

        Args:
            wall_id: The ID of the wall to check

        Returns:
            bool: True if wall with ID exists, False otherwise
        """
        return self.find_wall_by_id(wall_id) is not None

    def extend(self, other_list: 'ListWall'):
        """Extend the current list with walls from another list"""
        self.walls.extend(other_list.walls)
