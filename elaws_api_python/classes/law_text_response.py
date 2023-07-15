"""laws_and_ordinances
"""

import os
from typing import Optional
from xml.etree import ElementTree as ET

from .common import Result

SCHEMA_PATH: str = os.path.join(
    os.path.dirname(__file__),
    "../schema/full_text_of_laws_and_ordinances_schema.xsd"
)


class ApplData:
    """
    Main data information.

    Attributes
    ----------
    category : int, optional
        Law type category.
    law_name_list_info : LawNameListInfo
        List of law and ordinance information.
    """

    def __init__(
        self, law_id: Optional[str] = None,
        law_number: Optional[str] = None,
        law_full_text: Optional[str] = ET.Element,
        image_data: Optional[str] = None,
    ) -> None:
        """
        Initialize the ApplData object.

        Parameters
        ----------
        law_id : str, optional
            Law id.
        law_number : str, optional
            Law number.
        law_full_text : ET.Element, optional
            The full text.
        image_data : str, optional
            Image data.
        """
        self.law_id: Optional[str] = law_id
        self.law_number: Optional[str] = law_number
        self.law_full_text: Optional[ET.Element] = law_full_text
        self.image_data: Optional[str] = image_data

    @staticmethod
    def from_elem(elem: ET.Element):
        """
        Static method to create an ApplData object from an XML element.

        Parameters
        ----------
        elem : ET.Element
            XML element that contains the application data information.

        Returns
        -------
        ApplData
            ApplData object with the information from the XML element.
        """
        law_id = elem.find("LawId").text
        law_number = elem.find("LawId").text
        law_full_text = elem.find("LawFullText")
        image_data = elem.find("ImageData")
        return ApplData(law_id, law_number, law_full_text, image_data)


class LawTextResponse:
    """
    Root structure of the data obrained by `base.request_laws_and_ordinances`.

    Attributes
    ----------
    result : Result
        Processing result.
    appl_data : ApplData
        Main data.

    Parameters
    ----------
    xml_path : str
        Path to the XML data file.
    """

    def __init__(self, xml_content: str) -> None:
        """
        Initialize the DataRoot object by loading XML data from the specified path.

        Parameters
        ----------
        xml_content : str
            Content or path to the XML data file.
        """
        content = xml_content
        if os.path.exists(xml_content):
            with open(xml_content, "r", encoding="utf-8") as file_:
                content = file_.read()
        root = ET.fromstring(content)

        # XML data validation
        # schema = XMLSchema(SCHEMA_PATH)
        # if not schema.is_valid(root):
        #     raise ValueError("XML data does not conform to the schema.")

        # parse_data
        self._result: Optional[Result] = None
        self._appl_data: Optional[ApplData] = None
        self.parse_data(root)

    def parse_data(self, root: ET.Element) -> None:
        """
        Parse and extract data from the XML root element.

        Parameters
        ----------
        root : xml.etree.ElementTree.Element
            The root element of the XML data.
        """
        # Result
        result_element = root.find("Result")
        if result_element is None:
            raise ValueError("Result is not found.")
        self._result = Result.from_elem(result_element)

        # ApplData
        appl_data_element = root.find("ApplData")
        if appl_data_element is None:
            raise ValueError("ApplData is not found.")
        self._appl_data = ApplData.from_elem(appl_data_element)

    @property
    def result(self) -> Result:
        """
        Get the processing result information.

        Returns
        -------
        Result
            The processing result information.
        """
        return self._result

    @property
    def appl_data(self) -> ApplData:
        """
        Get the main data information.

        Returns
        -------
        ApplData
            The main data information.
        """
        return self._appl_data

    @property
    def law_full_text(self) -> ET.Element:
        """
        Get the full text.

        Returns
        -------
        ET.Element
            The full text.
        """
        return self._appl_data.law_full_text
