from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.images import get_image_model_string
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


@register_snippet
class Author(models.Model):
    """
    Author snippet for blog posts.
    
    Django model that mirrors the Jekyll authors.yml structure,
    storing author information including bio, avatar, and social links.
    
    Attributes
    ----------
    name : CharField
        Full name of the author.
    bio : TextField
        Short biographical description of the author.
    avatar : ForeignKey
        Profile image for the author.
    email : EmailField
        Author's email address.
    website : URLField
        Author's personal website URL.
    github : CharField
        GitHub username.
    linkedin : URLField
        LinkedIn profile URL.
    mastodon : URLField
        Mastodon profile URL.
    discord : URLField
        Discord profile URL.
    """
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, help_text="Short bio of the author")
    avatar = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Author's profile image"
    )
    
    # Social links
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    github = models.CharField(max_length=100, blank=True, help_text="GitHub username")
    linkedin = models.URLField(blank=True)
    mastodon = models.URLField(blank=True)
    discord = models.URLField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('bio'),
        FieldPanel('avatar'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('website'),
            FieldPanel('github'),
            FieldPanel('linkedin'),
            FieldPanel('mastodon'),
            FieldPanel('discord'),
        ], heading="Social Links")
    ]
    
    def __str__(self):
        """
        Return string representation of the author.
        
        Returns
        -------
        str
            Author's name.
        """
        return self.name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']


class BlogPageTag(TaggedItemBase):
    """
    Tag model for blog posts.
    
    Through model for many-to-many relationship between BlogPage and tags,
    enabling categorization of blog posts.
    
    Attributes
    ----------
    content_object : ParentalKey
        Reference to the BlogPage being tagged.
    """
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogIndexPage(Page):
    """
    Index page for blog posts.
    
    Wagtail page model for the main blog listing page that displays
    all published blog posts with pagination and filtering capabilities.
    """
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    class Meta:
        verbose_name = "Blog Index Page"


class BlogPage(Page):
    """
    Individual blog post page.
    
    Enhanced Wagtail page model for blog posts with complete Jekyll frontmatter
    support including author relationships, categories, header images, and SEO metadata.
    
    Attributes
    ----------
    date : DateField
        Publication date of the blog post.
    author : ForeignKey
        Author of the blog post.
    excerpt : TextField
        Brief description/summary of the post.
    body : RichTextField
        Main content of the blog post.
    header_image : ForeignKey
        Header/overlay image for the post.
    header_image_alt : CharField
        Alt text for the header image.
    custom_permalink : SlugField
        Custom URL path for the post.
    layout_classes : CharField
        CSS classes for layout styling.
    show_toc : BooleanField
        Whether to show table of contents.
    enable_comments : BooleanField
        Whether to enable comments.
    last_modified : DateField
        Date when post was last modified.
    tags : ClusterTaggableManager
        Tags/categories for the post.
    """
    date = models.DateField("Post date")
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts'
    )
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text="Brief description of the post (maps to Jekyll excerpt)"
    )
    body = RichTextField(blank=True)
    
    # Header image
    header_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Header/overlay image for the post"
    )
    header_image_alt = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alt text for header image"
    )
    
    # SEO and layout fields
    custom_permalink = models.SlugField(
        max_length=255,
        blank=True,
        help_text="Custom URL path (e.g., 'my-post.html')"
    )
    layout_classes = models.CharField(
        max_length=100,
        blank=True,
        default="wide",
        help_text="CSS classes for layout (e.g., 'wide')"
    )
    show_toc = models.BooleanField(
        default=True,
        help_text="Show table of contents"
    )
    enable_comments = models.BooleanField(
        default=True,
        help_text="Enable comments for this post"
    )
    
    # Last modified
    last_modified = models.DateField(
        blank=True,
        null=True,
        help_text="Date when post was last modified"
    )
    
    # Tags
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('author'),
        FieldPanel('excerpt'),
        FieldPanel('body'),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_image_alt'),
        ], heading="Header Image"),
        MultiFieldPanel([
            FieldPanel('custom_permalink'),
            FieldPanel('layout_classes'),
            FieldPanel('show_toc'),
            FieldPanel('enable_comments'),
            FieldPanel('last_modified'),
        ], heading="Layout & SEO"),
        FieldPanel('tags'),
    ]
    
    def get_permalink(self):
        """
        Return custom permalink or default URL.
        
        Returns
        -------
        str
            Custom permalink if set, otherwise default Wagtail URL.
        """
        if self.custom_permalink:
            return f"/blog/{self.custom_permalink}"
        return self.url
    
    @property
    def categories(self):
        """
        Return tags as categories for Jekyll compatibility.
        
        Returns
        -------
        list of str
            List of tag names associated with this post.
        """
        return [tag.name for tag in self.tags.all()]

    class Meta:
        verbose_name = "Blog Page"
        verbose_name_plural = "Blog Pages"


class EventPage(BlogPage):
    """
    Event page for workshops and events.
    
    Extends BlogPage with event-specific fields for start date, location,
    and event-specific metadata from Jekyll events posts.
    
    Attributes
    ----------
    start_date : DateField
        When the event starts.
    location : CharField
        Where the event takes place (e.g., "Online", "San Francisco").
    event_type : CharField
        Type of event (e.g., "workshop", "conference").
    """
    start_date = models.DateField(
        "Event start date",
        help_text="When the event starts"
    )
    location = models.CharField(
        max_length=255,
        default="Online",
        help_text="Event location (e.g., 'Online', 'San Francisco')"
    )
    event_type = models.CharField(
        max_length=100,
        default="event",
        help_text="Type of event (workshop, conference, etc.)"
    )
    
    content_panels = BlogPage.content_panels + [
        FieldPanel('start_date'),
        FieldPanel('location'),
        FieldPanel('event_type'),
    ]
    
    @property
    def is_event(self):
        """
        Return True to indicate this is an event page.
        
        Returns
        -------
        bool
            Always True for EventPage instances.
        """
        return True
    
    class Meta:
        verbose_name = "Event Page"
        verbose_name_plural = "Event Pages"
