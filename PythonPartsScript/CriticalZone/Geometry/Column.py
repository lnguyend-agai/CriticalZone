from .BaseElement import Cube
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

class RectangleColumn(Cube):
    def __init__(self, element_adapter: AllplanElementAdapter.BaseElementAdapter):
        super().__init__(element_adapter)
        self.point_at_end = []

    def is_wall_end(self):
        return bool(self.point_at_end)

class ListRectangleColumn:
    def __init__(self):
        self.columns = []

    def append(self, column: RectangleColumn):
        """Add a column to the list"""
        self.columns.append(column)

    def remove(self, column: RectangleColumn):
        """Remove a column from the list"""
        if column in self.columns:
            self.columns.remove(column)

    def get_column(self, index: int) -> RectangleColumn | None:
        """Get column at specific index"""
        if 0 <= index < len(self.columns):
            return self.columns[index]
        return None

    def get_all_columns(self) -> list:
        """Get all columns in the list"""
        return self.columns.copy()

    def clear(self):
        """Clear all columns from the list"""
        self.columns.clear()

    def count(self) -> int:
        """Get the number of columns in the list"""
        return len(self.columns)

    def is_empty(self) -> bool:
        """Check if the list is empty"""
        return len(self.columns) == 0

    def contains(self, column: RectangleColumn) -> bool:
        """Check if a column exists in the list"""
        return column in self.columns

    def __len__(self):
        """Return the number of columns"""
        return len(self.columns)

    def __getitem__(self, index):
        """Allow indexing access to columns"""
        return self.columns[index]

    def __iter__(self):
        """Make the list iterable"""
        return iter(self.columns)
    def find_column_by_id(self, column_id: str) -> RectangleColumn | None:
        """Find a column by its ID

        Args:
            column_id: The ID of the column to find

        Returns:
            RectangleColumn: The column if found, None otherwise
        """
        for column in self.columns:
            if hasattr(column, 'id') and column.id == column_id:
                return column
        return None

    def contains_column_by_id(self, column_id: str) -> bool:
        """Check if a column with the given ID exists in the list

        Args:
            column_id: The ID of the column to check

        Returns:
            bool: True if column with ID exists, False otherwise
        """
        return self.find_column_by_id(column_id) is not None

    def extend(self, other_list: 'ListRectangleColumn'):
        """Extend the current list with columns from another list"""
        self.columns.extend(other_list.columns)