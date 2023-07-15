"""common
"""

from typing import Optional
from xml.etree import ElementTree as ET


class Result:
    """
    Processing result information.

    Attributes
    ----------
    code : int, optional
        Code of the processing result.
    message : str, optional
        Message of the processing result.
    """

    def __init__(self, code: Optional[int] = None, message: Optional[str] = None) -> None:
        """
        Initialize the Result object.

        Parameters
        ----------
        code : int, optional
            Code of the processing result.
        message : str, optional
            Message of the processing result.
        """
        self.code: Optional[int] = code
        self.message: Optional[str] = message

    @staticmethod
    def from_elem(elem: ET.Element):
        """
        Static method to create a Result object from an XML element.

        Parameters
        ----------
        elem : xml.etree.ElementTree.Element
            XML element that contains the law information.

        Returns
        -------
        Result
            the Result object including the information in `elem`.
        """
        code = int(elem.find("Code").text)
        message = elem.find("Message").text
        return Result(code, message)
