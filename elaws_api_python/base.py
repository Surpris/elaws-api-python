"""elaws_api_python.base
"""

from typing import Optional
import requests

TIMEOUT_SEC = 30.0


def request_laws_and_ordinances(
    version: int, lawtype: int,
    timeout: float = TIMEOUT_SEC
) -> str:
    """
    Acquire a list of laws and ordinances.

    Parameters
    ----------
    version : int
        Version number of the e-Gov eLaw API.
    lawtype : int
        Law type.
    timeout : float, optional
        Timeout duration in seconds. Default is TIMEOUT_SEC.

    Returns
    -------
    str
        The list of laws and ordinances in the XML format.

    Raises
    ------
    requests.exceptions.RequestException
        If an error occurs during the API request.
    """
    url = f"https://elaws.e-gov.go.jp/api/{version}/lawlists/{lawtype}"

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def request_law_text(
    version: int, law_id_or_law_number: str,
    timeout: float = TIMEOUT_SEC
) -> str:
    """
    Acquire the full text of a law/ordinance.

    Parameters
    ----------
    version : int
        Version number of the e-Gov eLaw API.
    law_id_or_law_number : str
        Law ID or law number.

    Returns
    -------
    str
        The full text of the law/ordinance in the XML format.

    Raises
    ------
    requests.exceptions.RequestException
        If an error occurs during the API request.
    """
    url = f"https://elaws.e-gov.go.jp/api/{version}/lawdata/{law_id_or_law_number}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def request_law_content(
    version: int, law_number: Optional[str] = None,
    law_id: Optional[str] = None, article: Optional[str] = None,
    paragraph: Optional[str] = None, appdx_table: Optional[str] = None,
    timeout: float = TIMEOUT_SEC
) -> str:
    """
    Acquire the content of the current law/ordinance.

    Parameters
    ----------
    version : int
        Version number of the e-Gov eLaw API.
    law_number : str
        Law number.
    law_id : str
        Law ID.
    article : str, optional
        Article number. Defaults to None.
    paragraph : str, optional
        Paragraph number. Defaults to None.
    appdx_table : str, optional
        Appendix table number. Defaults to None.
    timeout : float, optional
        Timeout duration in seconds. Default is TIMEOUT_SEC.

    Returns
    -------
    str
        The content of the current law/ordinance in the XML format.

    Raises
    ------
    requests.exceptions.RequestException
        If an error occurs during the API request.
    ValueError
        If both law_number and law_id are given.
        Elst if the given combination of article, paragraph, and appdx_table
        is invalid.
    """
    if law_number and law_id:
        raise ValueError(
            "Only one of (law_number, law_id) is acceptable.")
    if (article and appdx_table) or (paragraph and appdx_table):
        raise ValueError(
            "Invalid combination of article, paragraph, and appdx_table.")

    url = f"https://elaws.e-gov.go.jp/api/{version}/articles;"
    if law_number is not None:
        url += f"lawNum={law_number};"
    if law_id is not None:
        url += f"lawId={law_id};"
    if article is not None:
        url += f"article={article};"
    if paragraph is not None:
        url += f"paragraph={paragraph};"
    if appdx_table is not None:
        url += f"appdxTable={appdx_table}"

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def request_list_of_updated_laws_and_ordinance(
    version: int, date: int,
    timeout: float = TIMEOUT_SEC
) -> str:
    """
    Acquire the full text of a law/ordinance.

    Parameters
    ----------
    version : int
        Version number of the e-Gov eLaw API.
    date : int
        date.

    Returns
    -------
    str
        The list of udpated laws and ordinances in the XML format.

    Raises
    ------
    requests.exceptions.RequestException
        If an error occurs during the API request.
    """
    url = f"https://elaws.e-gov.go.jp/api/{version}/updatelawlists/{date}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text
