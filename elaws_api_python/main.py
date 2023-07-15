"""elaws_api_python.main
"""

from .base import (
    request_laws_and_ordinances,
    request_law_text,
    TIMEOUT_SEC
)
from .classes import ListOfLaws, LawTextResponse


def acquire_laws_and_ordinances(
    version: int, lawtype: int,
    timeout: float = TIMEOUT_SEC
) -> ListOfLaws:
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
    ListOfLaws
        The list of laws and ordinances.
    """
    content = request_laws_and_ordinances(version, lawtype, timeout)
    return ListOfLaws(content)


def aquire_law_text(
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
    content = request_law_text(version, law_id_or_law_number, timeout)
    return LawTextResponse(content)
