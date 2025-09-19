from django.shortcuts import render, get_object_or_404
import logging

from .utils import (
    get_recent_contributors,
    get_recent_packages,
    generate_github_avatar_url,
    generate_github_profile_url
)
from publications.models import BlogPage, EventPage

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


def blog_index(request):
    """
    Blog index view for PyOpenSci.

    Static Django view that queries Wagtail BlogPage instances
    to display all blog posts in a consistent index page.

    Parameters
    ----------
    request : HttpRequest
        Django HTTP request object.

    Returns
    -------
    HttpResponse
        Rendered blog index page with blog posts.
    """
    blog_posts = BlogPage.objects.live().select_related('author').order_by('-date')

    context = {
        'page_title': 'pyOpenSci Blog',
        'hero_title': 'pyOpenSci Blog',
        'hero_subtitle': 'Here we will both post updates about pyOpenSci and also highlight contributors. We will also highlight new packages that have been reviewed and accepted into the pyOpenSci ecosystem.',
        'blog_posts': blog_posts,
    }
    return render(request, 'core/blog_index.html', context)


def events_index(request):
    """
    Events index view for PyOpenSci.

    Static Django view that queries Wagtail EventPage instances
    to display all events in a consistent index page.

    Parameters
    ----------
    request : HttpRequest
        Django HTTP request object.

    Returns
    -------
    HttpResponse
        Rendered events index page with events.
    """
    events = EventPage.objects.live().select_related('author').prefetch_related('tags').order_by('-start_date')

    context = {
        'page_title': 'pyOpenSci Events',
        'hero_title': 'pyOpenSci Events',
        'hero_subtitle': 'Join us for workshops, webinars, and community events. Connect with the scientific Python community and learn about open source best practices.',
        'events': events,
    }
    return render(request, 'core/events_index.html', context)


def serve_blog_page(request, slug):
    """
    Serve individual blog page with /blog/ prefix.

    Parameters
    ----------
    request : HttpRequest
        Django HTTP request object
    slug : str
        Page slug from URL

    Returns
    -------
    HttpResponse
        Rendered blog page using Wagtail's serve mechanism
    """
    page = get_object_or_404(BlogPage.objects.live().select_related('author'), slug=slug)
    return page.serve(request)


def serve_event_page(request, slug):
    """
    Serve individual event page with /events/ prefix.

    Parameters
    ----------
    request : HttpRequest
        Django HTTP request object
    slug : str
        Page slug from URL

    Returns
    -------
    HttpResponse
        Rendered event page using Wagtail's serve mechanism
    """
    page = get_object_or_404(EventPage.objects.live().select_related('author').prefetch_related('tags'), slug=slug)
    return page.serve(request)
