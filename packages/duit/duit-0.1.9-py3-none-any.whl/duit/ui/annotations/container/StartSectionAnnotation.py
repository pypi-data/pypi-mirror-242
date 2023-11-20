from typing import Optional

from duit.model.DataField import DataField
from duit.ui.annotations import UIAnnotation


class StartSectionAnnotation(UIAnnotation):
    def __init__(self, name: str, collapsed: bool = False, is_active_field: Optional[DataField[bool]] = None):
        """
        Initialize a StartSectionAnnotation.

        :param name: The name or title of the section.
        :param collapsed: Whether the section should be initially collapsed (default is False).
        :param is_active_field: An optional DataField that determines the active state of the section.
        """
        super().__init__(name, importance=5)
        self.collapsed = collapsed
        self.is_active_field = is_active_field
