from django.shortcuts import render
import logging

from .utils import (
    get_recent_contributors, 
    get_recent_packages,
    generate_github_avatar_url, 
    generate_github_profile_url
)

logger = logging.getLogger(__name__)


def home(request):
    """
    Homepage view for PyOpenSci.
    
    Parameters
    ----------
    request : HttpRequest
        Django HTTP request object.
        
    Returns
    -------
    HttpResponse
        Rendered home page with recent contributors data.
    """
    # Fetch recent contributors from YAML
    recent_contributors = get_recent_contributors(count=4)
    
    # Enhance contributor data with computed properties
    for contributor in recent_contributors:
        # Add avatar URL if github_image_id exists
        if contributor.get('github_image_id'):
            contributor['github_avatar_url'] = generate_github_avatar_url(
                contributor['github_image_id']
            )
        
        # Add profile URL
        contributor['github_profile_url'] = generate_github_profile_url(
            contributor['github_username']
        )
        
        # Add display name
        contributor['display_name'] = (
            contributor.get('name') or f"@{contributor['github_username']}"
        )

    # Fetch recent packages from YAML
    recent_packages = get_recent_packages(count=3)
    
    context = {
        'page_title': 'Welcome to pyOpenSci',
        'hero_title': 'We make it easier for scientists to create, find, maintain, and contribute to reusable code and software.',
        'hero_subtitle': 'pyOpenSci broadens participation in scientific open source by breaking down social and technical barriers. Join our global community.',
        # Used for the "New pyOpenSci contributors" section on the home page
        'recent_contributors': recent_contributors,
        # Used for the "Recently Accepted Python Packages" section on the home page
        'recent_packages': recent_packages,
    }
    return render(request, 'core/home.html', context)
