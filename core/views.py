from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

    # Fetch recent blog posts from Wagtail
    recent_blog_posts = (
        BlogPage.objects.live()
        .select_related('author')
        .order_by('-date')[:3]
    )

    context = {
        'page_title': 'Welcome to pyOpenSci',
        'hero_title': 'We make it easier for scientists to create, find, maintain, and contribute to reusable code and software.',
        'hero_subtitle': 'pyOpenSci broadens participation in scientific open source by breaking down social and technical barriers. Join our global community.',
        # Used for the "New pyOpenSci contributors" section on the home page
        'recent_contributors': recent_contributors,
        # Used for the "Recently Accepted Python Packages" section on the home page
        'recent_packages': recent_packages,
        # Used for the "Recent blog posts & updates" section on the home page
        'recent_blog_posts': recent_blog_posts,
    }
    return render(request, 'core/home.html', context)


def blog_index(request):
    """
    Blog index view for PyOpenSci.

    Static Django view that queries Wagtail BlogPage instances
    to display all blog posts in a consistent index page with pagination
    and optional year filtering.

    Parameters
    ----------
    request : HttpRequest
        Django HTTP request object.

    Returns
    -------
    HttpResponse
        Rendered blog index page with paginated blog posts.
    """
    # Get year filter from query params
    year_filter = request.GET.get('year')

    # Base queryset
    blog_posts = BlogPage.objects.live().select_related('author').order_by('-date')

    # Apply year filter if provided
    if year_filter and year_filter.isdigit():
        blog_posts = blog_posts.filter(date__year=int(year_filter))

    # Get available years for filter dropdown
    available_years = (
        BlogPage.objects.live()
        .dates('date', 'year', order='DESC')
    )

    # Pagination: 12 posts per page
    paginator = Paginator(blog_posts, 12)
    page = request.GET.get('page')

    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'page_title': 'pyOpenSci Blog',
        'hero_title': 'pyOpenSci Blog',
        'hero_subtitle': 'Here we will both post updates about pyOpenSci and also highlight contributors. We will also highlight new packages that have been reviewed and accepted into the pyOpenSci ecosystem.',
        'blog_posts': paginated_posts,
        'available_years': available_years,
        'selected_year': year_filter,
    }
    return render(request, 'core/blog_index.html', context)


def events_index(request):
    """
    Events index view for PyOpenSci.

    Static Django view that queries Wagtail EventPage instances
    to display all events in a consistent index page with pagination
    and optional year filtering.

    Parameters
    ----------
    request : HttpRequest
        Django HTTP request object.

    Returns
    -------
    HttpResponse
        Rendered events index page with paginated events.
    """
    # Get year filter from query params
    year_filter = request.GET.get('year')

    # Base queryset
    events = EventPage.objects.live().select_related('author').prefetch_related('tags').order_by('-start_date')

    # Apply year filter if provided
    if year_filter and year_filter.isdigit():
        events = events.filter(start_date__year=int(year_filter))

    # Get available years for filter dropdown
    available_years = (
        EventPage.objects.live()
        .dates('start_date', 'year', order='DESC')
    )

    # Pagination: 15 events per page
    paginator = Paginator(events, 15)
    page = request.GET.get('page')

    try:
        paginated_events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_events = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_events = paginator.page(paginator.num_pages)

    # Separate upcoming and past events
    from django.utils import timezone
    today = timezone.now().date()

    upcoming_events = EventPage.objects.live().filter(start_date__gte=today).select_related('author').prefetch_related('tags').order_by('start_date')

    context = {
        'page_title': 'pyOpenSci Events',
        'hero_title': 'pyOpenSci Events',
        'hero_subtitle': 'pyOpenSci holds events that support scientists developing open science skills.',
        'events': paginated_events,
        'upcoming_events': upcoming_events,
        'available_years': available_years,
        'selected_year': year_filter,
        'today': today,
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
    page = get_object_or_404(BlogPage.objects.live().select_related('author').prefetch_related('tags'), slug=slug)

    # Get related posts based on tag overlap
    page_tags = page.tags.all()
    related_posts = []

    if page_tags:
        # Find posts with overlapping tags
        from django.db.models import Count
        related_posts = (
            BlogPage.objects.live()
            .select_related('author')
            .prefetch_related('tags')
            .filter(tags__in=page_tags)
            .exclude(pk=page.pk)
            .annotate(same_tags=Count('pk'))
            .order_by('-same_tags', '-date')[:3]
        )

    # Fallback to recent posts if no tag matches
    if not related_posts:
        related_posts = (
            BlogPage.objects.live()
            .select_related('author')
            .exclude(pk=page.pk)
            .order_by('-date')[:3]
        )

    # Add related_posts to the page context
    page.related_posts = related_posts

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

    # Get related events based on tag overlap
    page_tags = page.tags.all()
    related_events = []

    if page_tags:
        # Find events with overlapping tags
        from django.db.models import Count
        related_events = (
            EventPage.objects.live()
            .select_related('author')
            .prefetch_related('tags')
            .filter(tags__in=page_tags)
            .exclude(pk=page.pk)
            .annotate(same_tags=Count('pk'))
            .order_by('-same_tags', '-start_date')[:3]
        )

    # Fallback to recent events if no tag matches
    if not related_events:
        related_events = (
            EventPage.objects.live()
            .select_related('author')
            .exclude(pk=page.pk)
            .order_by('-start_date')[:3]
        )

    # Add related_events to the page context
    page.related_events = related_events

    return page.serve(request)
