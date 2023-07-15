"""elaws_api_python.main
"""

from .base import (
    request_laws_and_ordinances,
    TIMEOUT_SEC
)
from .classes import ListOfLaws


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
