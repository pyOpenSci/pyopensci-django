"""
Utility functions for working with contributor and package data.

This module provides functions to fetch and parse contributor and package data from YAML files,
following the same format used by the Jekyll site and pyosMeta package.
"""

from ruamel.yaml import YAML, YAMLError
import logging
from typing import List, Dict, Any
from urllib.request import urlopen
from urllib.error import URLError
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize YAML parser with safe loading
yaml = YAML(typ='safe')


class ContributorDataError(Exception):
    """Custom exception for contributor data related errors."""
    pass


class PackageDataError(Exception):
    """Custom exception for package data related errors."""
    pass


def fetch_contributors_yaml(url: str = None) -> List[Dict[str, Any]]:
    """
    Fetch contributor data from YAML source.
    
    Parameters
    ----------
    url : str, optional
        URL to fetch YAML from. If None, uses the default pyOpenSci GitHub URL.
        
    Returns
    -------
    list of dict
        List of contributor dictionaries.
        
    Raises
    ------
    ContributorDataError
        If data cannot be fetched or parsed.
    """
    if url is None:
        url = "https://raw.githubusercontent.com/pyOpenSci/pyopensci.github.io/main/_data/contributors.yml"
    
    try:
        with urlopen(url) as response:
            yaml_content = response.read().decode('utf-8')
            contributors = yaml.load(yaml_content)
            
        if not isinstance(contributors, list):
            raise ContributorDataError("YAML data should be a list of contributors")
            
        logger.info(f"Successfully fetched {len(contributors)} contributors from {url}")
        return contributors
        
    except URLError as e:
        logger.error(f"Failed to fetch contributors from {url}: {e}")
        raise ContributorDataError(f"Network error: {e}")
    except YAMLError as e:
        logger.error(f"Failed to parse YAML: {e}")
        raise ContributorDataError(f"YAML parsing error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching contributors: {e}")
        raise ContributorDataError(f"Unexpected error: {e}")



def get_recent_contributors(count: int = 4) -> List[Dict[str, Any]]:
    """
    Get the most recent contributors.
    
    Parameters
    ----------
    count : int, default 4
        Number of recent contributors to return.
        
    Returns
    -------
    list of dict
        List of recent contributor dictionaries, sorted by date_added descending.
    """
    try:
        contributors = fetch_contributors_yaml()
        
        # Return most recent contributors (last items in list)
        reversed_contributors = list(reversed(contributors))
        
        return reversed_contributors[:count]
        
    except ContributorDataError as e:
        logger.error(f"Failed to get recent contributors: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error getting recent contributors: {e}")
        return []


def fetch_packages_yaml(url=None):
    """
    Fetch package data from YAML source.
    
    Parameters
    ----------
    url : str, optional
        URL to fetch YAML from. If None, uses the default pyOpenSci GitHub URL.
        
    Returns
    -------
    list of dict
        List of package dictionaries.
        
    Raises
    ------
    ContributorDataError
        If data cannot be fetched or parsed.
    """
    if url is None:
        url = "https://raw.githubusercontent.com/pyOpenSci/pyopensci.github.io/main/_data/packages.yml"
    
    try:
        with urlopen(url) as response:
            yaml_content = response.read().decode('utf-8')
            packages = yaml.load(yaml_content)
            
        if not isinstance(packages, list):
            raise PackageDataError("YAML data should be a list of packages")
            
        logger.info(f"Successfully fetched {len(packages)} packages from {url}")
        return packages
        
    except URLError as e:
        logger.error(f"Failed to fetch packages from {url}: {e}")
        raise PackageDataError(f"Network error: {e}")
    except YAMLError as e:
        logger.error(f"Failed to parse YAML: {e}")
        raise PackageDataError(f"YAML parsing error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching packages: {e}")
        raise PackageDataError(f"Unexpected error: {e}")


def get_recent_packages(count=3):
    """
    Get the most recently accepted packages.
    
    Parameters
    ----------
    count : int, default 3
        Number of recent packages to return.
        
    Returns
    -------
    list of dict
        List of recent package dictionaries, sorted by date_accepted descending.
    """
    try:
        packages = fetch_packages_yaml()
        
        # Sort packages by date_accepted descending (most recent first)
        sorted_packages = sorted(packages, key=lambda x: x.get('date_accepted', ''), reverse=True)
        
        return sorted_packages[:count]
        
    except PackageDataError as e:
        logger.error(f"Failed to get recent packages: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error getting recent packages: {e}")
        return []


def generate_github_avatar_url(github_image_id: int) -> str:
    """
    Generate GitHub avatar URL from image ID.
    
    Parameters
    ----------
    github_image_id : int
        GitHub user's image ID.
        
    Returns
    -------
    str
        GitHub avatar URL.
    """
    return f"https://avatars.githubusercontent.com/u/{github_image_id}?s=400&v=4"


def generate_github_profile_url(github_username: str) -> str:
    """
    Generate GitHub profile URL from username.
    
    Parameters
    ----------
    github_username : str
        GitHub username.
        
    Returns
    -------
    str
        GitHub profile URL.
    """
    return f"https://github.com/{github_username}"


