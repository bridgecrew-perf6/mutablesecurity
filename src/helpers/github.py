"""Module for interacting with GitHub API."""
import json

import requests

from src.helpers.exceptions import GitHubAPIError, NoIdentifiedAssetException


def __get_latest_release(username: str, repository: str) -> dict:
    """Get the latest GitHub release.

    Args:
        username (str): GitHub user's name
        repository (str): Repository's name

    Raises:
        GitHubAPIError: The GitHub reponse is not successful.

    Returns:
        dict: Returned dictionary
    """
    connection = requests.get(
        f"https://api.github.com/repos/{username}/{repository}/releases/latest"
    )
    if connection.status_code != 200:
        raise GitHubAPIError()

    return json.loads(connection.content)


def get_latest_release_name(username: str, repository: str) -> str:
    """Get the latest release name from a repositry.

    Args:
        username (str): GitHub user's name
        repository (str): Repository's name

    Returns:
        str: Name of the release
    """
    release = __get_latest_release(username, repository)

    return release["name"]


def get_asset_from_latest_release(
    username: str, repository: str, unique_name_part: str
) -> str:
    """Get the first asset having a string in its name.

    Args:
        username (str): GitHub user's name
        repository (str): Repository's name
        unique_name_part (str): Release name identifier

    Raises:
        NoIdentifiedAssetException: No asset was identified.

    Returns:
        str: Download URL
    """
    release = __get_latest_release(username, repository)
    assets = release["assets"]

    for asset in assets:
        if unique_name_part in asset["name"]:
            return asset["browser_download_url"]

    raise NoIdentifiedAssetException()
