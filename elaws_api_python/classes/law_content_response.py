"""laws_and_ordinances
"""

import os
from typing import Optional, List
from xml.etree import ElementTree as ET

from .common import Result

SCHEMA_PATH: str = os.path.join(
    os.path.dirname(__file__),
    "../schema/schema.xsd"
)


class AppdxTableTitle:
    def __init__(self, appdx_table_title: Optional[ET.Element] = None) -> None:
        self.appdx_table_title: Optional[ET.Element] = appdx_table_title

    @staticmethod
    def from_elem(elem: ET.Element):
        return AppdxTableTitle(elem)


class AppdxTableTitleList:
    def __init__(self, table_title_list: Optional[List[AppdxTableTitle]] = None) -> None:
        self._table_title_list: Optional[List[AppdxTableTitle]] = table_title_list

    @staticmethod
    def from_elem(elem: ET.Element):
        table_list = [
            AppdxTableTitle.from_elem(elem)
            for elem in elem.findall("AppdxTableTitle")
        ]
        return AppdxTableTitleList(table_list)

    @property
    def table_title_list(self) -> List[AppdxTableTitle]:
        return self._table_title_list


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
        article: Optional[str] = None,
        paragraph: Optional[str] = None,
        appdx_table: Optional[str] = None,
        law_contents: Optional[ET.Element] = None,
        appdx_table_title_list: Optional[AppdxTableTitleList] = None,
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
        self.article: Optional[str] = article
        self.paragraph: Optional[str] = paragraph
        self.appdx_table: Optional[str] = appdx_table
        self.law_contents: Optional[ET.Element] = law_contents
        self.appdx_table_title_list: Optional[AppdxTableTitleList] = appdx_table_title_list
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
        law_number = elem.find("LawNum").text
        article = elem.find("Article").text
        paragraph = elem.find("Paragraph").text
        appdx_table = elem.find("AppdxTable").text
        law_contents = elem.find("LawContents")
        appdx_table_title_list = elem.find("AppdxTableTitleLists")
        if appdx_table_title_list:
            appdx_table_title_list = AppdxTableTitleList.from_elem(
                appdx_table_title_list
            )

        image_data = elem.find("ImageData")
        if image_data:
            image_data = image_data.text
        return ApplData(
            law_id, law_number, article, paragraph,
            appdx_table, law_contents,
            appdx_table_title_list, image_data
        )


class LawContentResponse:
    """
    Root structure of the data obrained by `base.request_law_content`.

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
