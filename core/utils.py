"""
Utility functions for working with contributor data.

This module provides functions to fetch and parse contributor data from YAML files,
following the same format used by the Jekyll site and pyosMeta package.
"""

import yaml
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.request import urlopen
from urllib.error import URLError

logger = logging.getLogger(__name__)


class ContributorDataError(Exception):
    """Custom exception for contributor data related errors."""
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
            contributors = yaml.safe_load(yaml_content)
            
        if not isinstance(contributors, list):
            raise ContributorDataError("YAML data should be a list of contributors")
            
        logger.info(f"Successfully fetched {len(contributors)} contributors from {url}")
        return contributors
        
    except URLError as e:
        logger.error(f"Failed to fetch contributors from {url}: {e}")
        raise ContributorDataError(f"Network error: {e}")
    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML: {e}")
        raise ContributorDataError(f"YAML parsing error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching contributors: {e}")
        raise ContributorDataError(f"Unexpected error: {e}")


def parse_contributor_date(date_str: Any) -> Optional[datetime]:
    """
    Parse a date string into a datetime object.
    
    Parameters
    ----------
    date_str : Any
        Date string in various formats.
        
    Returns
    -------
    datetime or None
        Parsed datetime object or None if parsing fails.
    """
    if not date_str:
        return None
        
    # Convert to string if it's not already
    date_str = str(date_str).strip()
    
    # Try common date formats
    date_formats = [
        '%Y-%m-%d',
        '%Y/%m/%d', 
        '%m/%d/%Y',
        '%d/%m/%Y'
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
            
    logger.warning(f"Could not parse date: {date_str}")
    return None


def clean_contributor_data(contributor: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and normalize contributor data.
    
    Parameters
    ----------
    contributor : dict
        Raw contributor dictionary from YAML.
        
    Returns
    -------
    dict
        Cleaned contributor dictionary.
    """
    cleaned = {}
    
    # Required field
    if 'github_username' not in contributor:
        raise ContributorDataError("Contributor missing required field: github_username")
    
    cleaned['github_username'] = contributor['github_username']
    
    # String fields - strip whitespace
    string_fields = [
        'name', 'bio', 'organization', 'location', 'email',
        'twitter', 'mastodon', 'orcidid', 'website'
    ]
    
    for field in string_fields:
        value = contributor.get(field)
        if value and str(value).strip():
            cleaned[field] = str(value).strip()
    
    # Integer fields
    for field in ['github_image_id', 'sort']:
        value = contributor.get(field)
        if value is not None:
            try:
                cleaned[field] = int(value)
            except (ValueError, TypeError):
                logger.warning(f"Invalid {field} for {contributor.get('github_username')}: {value}")
    
    # Date field
    date_added = contributor.get('date_added')
    if date_added:
        parsed_date = parse_contributor_date(date_added)
        if parsed_date:
            cleaned['date_added'] = parsed_date.date()
    
    # Boolean fields
    boolean_fields = [
        'deia_advisory', 'editorial_board', 'emeritus_editor',
        'advisory', 'emeritus_advisory', 'board'
    ]
    
    for field in boolean_fields:
        value = contributor.get(field)
        if value is not None:
            cleaned[field] = bool(value)
    
    # List fields - ensure they're lists
    list_fields = [
        'title', 'partners', 'contributor_type', 'packages_eic',
        'packages_editor', 'packages_submitted', 'packages_reviewed'
    ]
    
    for field in list_fields:
        value = contributor.get(field, [])
        if value is None:
            cleaned[field] = []
        elif isinstance(value, list):
            # Filter out empty/None values and strip strings
            cleaned[field] = [
                str(item).strip() for item in value 
                if item is not None and str(item).strip()
            ]
        else:
            # Single value, convert to list
            cleaned[field] = [str(value).strip()] if str(value).strip() else []
    
    return cleaned


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
        
        # Clean all contributor data
        cleaned_contributors = []
        for contributor in contributors:
            try:
                cleaned = clean_contributor_data(contributor)
                cleaned_contributors.append(cleaned)
            except ContributorDataError as e:
                logger.warning(f"Skipping invalid contributor: {e}")
                continue
        
        # Sort by date_added (newest first), then by sort field
        def sort_key(contributor):
            date_added = contributor.get('date_added')
            sort_value = contributor.get('sort', 999999)  # Default high sort value
            
            # Contributors without dates go to the end
            if date_added is None:
                return (datetime.min.date(), sort_value)
            
            return (date_added, sort_value)
        
        sorted_contributors = sorted(
            cleaned_contributors, 
            key=sort_key, 
            reverse=True
        )
        
        return sorted_contributors[:count]
        
    except ContributorDataError as e:
        logger.error(f"Failed to get recent contributors: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error getting recent contributors: {e}")
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