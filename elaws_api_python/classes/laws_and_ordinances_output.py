"""laws_and_ordinances_output
"""

import os
from typing import List, Optional, Dict
from xml.etree import ElementTree as ET
from xmlschema import XMLSchema


SCHEMA_PATH: str = os.path.join(
    os.path.dirname(__file__),
    "../schema/laws_and_odinances_output.xsd"
)


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


class LawNameInfoElement:
    """
    Information about a law/ordinance.

    Attributes
    ----------
    law_id : str, optional
        Law ID.
    law_name : str, optional
        Law name.
    law_number : str, optional
        Law number.
    promulgation_date : str, optional
        Promulgation date.
    """

    def __init__(
        self, law_id: Optional[str] = None, law_name: Optional[str] = None,
        law_number: Optional[str] = None, promulgation_date: Optional[str] = None
    ) -> None:
        """
        Initialize the LawNameInfoElement object.

        Parameters
        ----------
        law_id : str, optional
            Law ID.
        law_name : str, optional
            Law name.
        law_number : str, optional
            Law number.
        promulgation_date : str, optional
            Promulgation date.
        """
        self.law_id: Optional[str] = law_id
        self.law_name: Optional[str] = law_name
        self.law_number: Optional[str] = law_number
        self.promulgation_date: Optional[str] = promulgation_date

    @staticmethod
    def from_elem(elem: ET.Element):
        """
        Static method to create a LawNameInfoElement object from an XML element.

        Parameters
        ----------
        elem : xml.etree.ElementTree.Element
            XML element that contains the law information.

        Returns
        -------
        LawNameInfoElement
            LawNameInfoElement object with the information from the XML element.
        """
        law_id = elem.find("LawId").text
        law_name = elem.find("LawName").text
        law_number = elem.find("LawNum").text
        promulgation_date = elem.find("PromulgationDate").text
        return LawNameInfoElement(law_id, law_name, law_number, promulgation_date)


class LawNameListInfo:
    """
    List of information about law/ordinance.

    Attributes
    ----------
    list_of_info : List[LawNameInfoElement]
        List of information about law/ordinance.
    """

    def __init__(self, list_of_info: Optional[List[LawNameInfoElement]] = None) -> None:
        """
        Initialize the LawNameListInfo object.

        Parameters
        ----------
        list_of_info : List[LawNameInfoElement], optional
             List of information about law/ordinance.
        """
        self._list_of_info: List[LawNameInfoElement] = list_of_info
        self._index_cache_by_law_name: Dict[str, int] = {}
        self._index_cache_by_keyword: Dict[str, List[int]] = {}
        self._index_cache_by_law_id: Dict[str, int] = {}

    def __iter__(self):
        return self._list_of_info.__iter__

    @staticmethod
    def from_elem(elem: ET.Element):
        """
        Static method to create a LawNameInfoElement object from an XML element.

        Parameters
        ----------
        elem : xml.etree.ElementTree.Element
            XML element that contains a list of law/ordinance information.

        Returns
        -------
        LawNameInfoElement
            LawNameInfoElement object with the information from the XML element.
        """
        list_ = [
            LawNameInfoElement(law_info_elem)
            for law_info_elem in elem.findall("LawNameListInfo")
        ]
        return LawNameListInfo(list_)

    def find_element_by_law_id(self, law_id: str) -> Optional[LawNameInfoElement]:
        """
        Find the law information element by law id.

        Parameters
        ----------
        law_id : str
            The id of the law/ordinance.

        Returns
        -------
        LawNameInfoElement, optional
            If the law/ordinance with the specified id exists, its information is returned.
            If no such law/ordinance exists, None is returned.
        """
        index = self._index_cache_by_law_id.get(law_id, "")
        if index:
            return self._list_of_info[index]

        for index, elem in enumerate(self._list_of_info):
            if law_id == elem.law_id:
                self._index_cache_by_keyword[law_id] = index
                return elem
        return None

    def find_law_name_by_law_id(self, law_id: str) -> Optional[str]:
        """
        Find the law name by law id.

        Parameters
        ----------
        law_id : str
            The id of the law/ordinance.

        Returns
        -------
        str, optional
            If the law/ordinance with the specified id exists, its naem is returned.
            If no such law/ordinance exists, None is returned.
        """
        elem = self.find_element_by_law_id(law_id)
        if elem is not None:
            return elem.law_name
        return None

    def find_element_by_law_name(self, law_name: str) -> Optional[LawNameInfoElement]:
        """
        Find the law information element by law name.

        Parameters
        ----------
        law_name : str
            The name of the law/ordinance.

        Returns
        -------
        LawNameInfoElement, optional
            If the law/ordinance with the specified law name exists, its information is returned.
            If no such law/ordinance exists, None is returned.
        """
        index = self._index_cache_by_law_name.get(law_name, None)
        if index:
            return self._list_of_info[index]

        for index, elem in enumerate(self._list_of_info):
            if law_name == elem.law_name:
                self._index_cache_by_law_name[law_name] = index
                return elem
        return None

    def find_law_id_by_law_name(self, law_name: str) -> Optional[str]:
        """
        Find the law id by law name.

        Parameters
        ----------
        law_name : str
            The name of the law/ordinance.

        Returns
        -------
        str, optional
            If the law/ordinance with the specified id exists, its id is returned.
            If no such law/ordinance exists, None is returned.
        """
        elem = self.find_element_by_law_name(law_name)
        if elem is not None:
            return elem.law_id
        return None

    def findall_elements_by_keyword_in_law_name(self, key: str) -> List[LawNameInfoElement]:
        """
        Find all the law information elements whose names include `key.`

        Parameters
        ----------
        key : str
            The keyword of the law/ordinance.

        Returns
        -------
        List[LawNameInfoElement]
            List of the law information elements whose names include 'key.'
        """
        index = self._index_cache_by_keyword.get(key, None)
        if index:
            return [self._list_of_info[ii] for ii in index]

        index_list: List[int] = []
        dst: List[str] = []
        for index, elem in enumerate(self._list_of_info):
            if key in elem.law_name:
                index_list.append(index)
                dst.append(elem)
        self._index_cache_by_keyword[key] = index_list
        return dst

    def findall_law_ids_by_keyword_in_law_name(self, key: str) -> List[str]:
        """
        Find all the law ids of the law information elements whose names include 'key.'

        Parameters
        ----------
        key : str
            The keyword of the law/ordinance.

        Returns
        -------
        List[str]
            List of law ids of the law information elements whose names include 'key.'
        """
        return [elem.law_id for elem in self.findall_elements_by_keyword_in_law_name(key)]

    def findall_law_names_by_keyword_in_law_name(self, key: str) -> List[str]:
        """
        Find all the law names of the law information elements including 'key.'

        Parameters
        ----------
        key : str
            The keyword of the law/ordinance.

        Returns
        -------
        List[str]
            List of law names of the law information elements including 'key.'
        """
        return [elem.law_name for elem in self.findall_elements_by_keyword_in_law_name(key)]

    @property
    def list_of_info(self):
        """
        A list of LawNameInfoElement.
        """
        return self._list_of_info

    @property
    def law_ids(self):
        """
        A list of law ids.
        """
        return [elem.law_id for elem in self._list_of_info]

    @property
    def law_names(self):
        """
        A list of law names.
        """
        return [elem.law_name for elem in self._list_of_info]


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
        self, category: Optional[int] = None,
        law_name_list_info: Optional[LawNameListInfo] = None
    ) -> None:
        """
        Initialize the ApplData object.

        Parameters
        ----------
        category : int, optional
            Law type category.
        law_name_list_info : List[LawNameInfoElement], optional
            List of laws and ordinances information.
        """
        self.category: Optional[int] = category
        self.law_name_list_info: LawNameListInfo = law_name_list_info

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
        category = int(elem.find("Category").text)
        law_name_list_info = LawNameListInfo.from_elem(elem)
        return ApplData(category, law_name_list_info)


class DataRoot:
    """
    Root data structure.

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

    def __init__(self, xml_path: str) -> None:
        """
        Initialize the DataRoot object by loading XML data from the specified path.
        
        Parameters
        ----------
        xml_path : str
            Path to the XML data file.
        """

        # XML data validation
        schema = XMLSchema(SCHEMA_PATH)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        if not schema.is_valid(root):
            raise ValueError("XML data does not conform to the schema.")

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
        self._result.code = int(result_element.find("Code").text)
        self._result.message = result_element.find("Message").text

        # ApplData
        appl_data_element = root.find("ApplData")
        if appl_data_element is None:
            raise ValueError("ApplData is not found.")
        self._appl_data = ApplData.from_elem(appl_data_element)
    
    def find_element_by_law_id(self, law_id: str) -> Optional[LawNameInfoElement]:
        """
        Find the law information element by law id.

        Parameters
        ----------
        law_id : str
            The id of the law/ordinance.

        Returns
        -------
        LawNameInfoElement, optional
            If the law/ordinance with the specified id exists, its information is returned.
            If no such law/ordinance exists, None is returned.
        """
        return self.appl_data.law_name_list_info.find_element_by_law_id(law_id)

    def find_law_name_by_law_id(self, law_id: str) -> Optional[str]:
        """
        Find the law name by law id.

        Parameters
        ----------
        law_id : str
            The id of the law/ordinance.

        Returns
        -------
        str, optional
            If the law/ordinance with the specified id exists, its naem is returned.
            If no such law/ordinance exists, None is returned.
        """
        return self.appl_data.law_name_list_info.find_law_name_by_law_id(law_id)

    def find_element_by_law_name(self, law_name: str) -> Optional[LawNameInfoElement]:
        """
        Find the law information element by law name.

        Parameters
        ----------
        law_name : str
            The name of the law/ordinance.

        Returns
        -------
        LawNameInfoElement, optional
            If the law/ordinance with the specified law name exists, its information is returned.
            If no such law/ordinance exists, None is returned.
        """
        return self.appl_data.law_name_list_info.find_element_by_law_name(law_name)

    def find_law_id_by_law_name(self, law_name: str) -> Optional[str]:
        """
        Find the law id by law name.

        Parameters
        ----------
        law_name : str
            The name of the law/ordinance.

        Returns
        -------
        str, optional
            If the law/ordinance with the specified id exists, its id is returned.
            If no such law/ordinance exists, None is returned.
        """
        return self.appl_data.law_name_list_info.find_law_id_by_law_name(law_name)

    def findall_elements_by_keyword_in_law_name(self, key: str) -> List[LawNameInfoElement]:
        """
        Find all the law information elements whose names include `key.`

        Parameters
        ----------
        key : str
            The keyword of the law/ordinance.

        Returns
        -------
        List[LawNameInfoElement]
            List of the law information elements whose names include 'key.'
        """
        return self.appl_data.law_name_list_info.findall_elements_by_keyword_in_law_name(key)

    def findall_law_ids_by_keyword_in_law_name(self, key: str) -> List[str]:
        """
        Find all the law ids of the law information elements whose names include 'key.'

        Parameters
        ----------
        key : str
            The keyword of the law/ordinance.

        Returns
        -------
        List[str]
            List of law ids of the law information elements whose names include 'key.'
        """
        return self.appl_data.law_name_list_info.findall_law_ids_by_keyword_in_law_name(key)

    def findall_law_names_by_keyword_in_law_name(self, key: str) -> List[str]:
        """
        Find all the law names of the law information elements including 'key.'

        Parameters
        ----------
        key : str
            The keyword of the law/ordinance.

        Returns
        -------
        List[str]
            List of law names of the law information elements including 'key.'
        """
        return self.appl_data.law_name_list_info.findall_law_names_by_keyword_in_law_name(key)

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
    def list_name_list_info(self) -> List[LawNameInfoElement]:
        """
        Get a list of law/ordinance information.

        Returns
        -------
        list
            A list of LawNameInfoElement instances.
        """
        return self._appl_data.law_name_list_info.list_of_info
