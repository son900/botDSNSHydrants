"""
Base import service.
"""

import logging
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.worksheet import worksheet


logger = logging.getLogger(__name__)


class BaseImportService:
    """
    Base class to import from xlsx files.

    It implements methods that are common to all descendant classes.

    """

    @staticmethod
    def get_sheet(
        file,
    ) -> worksheet:
        """
        Read xlsx file and return first sheet.
        """
        workbook = load_workbook(BytesIO(file))
        sheet = workbook.active
        return sheet

    @staticmethod
    def validate_row(
        row,
    ) -> bool:
        """
        Check if row is valid.
        """
        rows = [row[i] for i in range(4)]
        if any(element is None for element in rows):
            return False
        return True

