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
    version: int, law_id_or_law_number: str,
    article: Optional[str] = None, paragraph: Optional[str] = None,
    appdx_table: Optional[str] = None, timeout: float = TIMEOUT_SEC
) -> str:
    """
    Acquire the content of the current law/ordinance.

    Parameters
    ----------
    version : int
        Version number of the e-Gov eLaw API.
    law_id_or_law_number : str
        Law ID or law number.
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
        If the given combination of article, paragraph, and appdx_table
        is invalid.
    """
    if (article and appdx_table) or (paragraph and appdx_table):
        raise ValueError(
            "Invalid combination of article, paragraph, and appdx_table.")

    url = f"https://elaws.e-gov.go.jp/api/{version}/articles;"
    url += f"lawNum={law_id_or_law_number};"
    url += f"article={article};"
    url += f"paragraph={paragraph};"
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
