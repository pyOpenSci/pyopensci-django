from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


@register_snippet
class Author(models.Model):
    """
    Author snippet for blog posts and events.

    Reusable snippet containing author information that can be referenced
    by blog posts and events. Based on Jekyll's _data/authors.yml structure.

    Attributes
    ----------
    name : CharField
        The author's full name as it appears in bylines
    slug : SlugField
        URL-safe version of the author's name, unique identifier
    bio : TextField
        Short biographical description of the author
    avatar : ImageField
        Profile photo of the author
    email : EmailField
        Author's contact email address
    website : URLField
        Personal or professional website URL
    github : CharField
        GitHub username (without @ symbol)
    linkedin : URLField
        LinkedIn profile URL
    mastodon : CharField
        Mastodon handle (without @ symbol)
    discord : CharField
        Discord username
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    bio = models.TextField(blank=True, help_text="Short bio of the author")
    avatar = models.ImageField(upload_to='authors/', blank=True, null=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    github = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    mastodon = models.CharField(max_length=100, blank=True)
    discord = models.CharField(max_length=100, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('bio'),
        FieldPanel('avatar'),
        FieldPanel('email'),
        FieldPanel('website'),
        FieldPanel('github'),
        FieldPanel('linkedin'),
        FieldPanel('mastodon'),
        FieldPanel('discord'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class BlogPageTag(TaggedItemBase):
    """
    Tag model for blog posts.

    Enables tagging functionality for blog posts using django-taggit.
    """
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class EventPageTag(TaggedItemBase):
    """
    Tag model for event pages.

    Enables tagging functionality for event pages using django-taggit.
    """
    content_object = ParentalKey(
        'EventPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    """
    Individual blog post page.

    Page model for individual blog posts with full Jekyll frontmatter compatibility.
    Supports authors, categories/tags, header images, and rich content.

    Attributes
    ----------
    date : DateField
        Publication date of the blog post
    last_modified : DateTimeField
        Last modification timestamp
    author : ForeignKey
        Reference to Author snippet
    excerpt : TextField
        Short description/summary of the post
    header_image : ImageField
        Featured image for the post
    header_image_alt : CharField
        Alt text for the header image
    body : RichTextField
        Main content of the blog post
    enable_comments : BooleanField
        Whether to show comments section
    tags : ClusterTaggableManager
        Categories/tags for the post
    """
    date = models.DateField("Post date", help_text="Date when the post was published")
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        'Author',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blog_posts'
    )
    excerpt = models.TextField(
        blank=True,
        max_length=500,
        help_text="Brief description of the post"
    )
    header_image = models.ImageField(
        upload_to='blog/headers/',
        blank=True,
        null=True,
        help_text="Featured image for the post"
    )
    header_image_alt = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alt text for the header image"
    )
    body = RichTextField(blank=True)
    enable_comments = models.BooleanField(
        default=False,
        help_text="Show comments section on this post"
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('author'),
        FieldPanel('excerpt'),
        FieldPanel('header_image'),
        FieldPanel('header_image_alt'),
        FieldPanel('body'),
        FieldPanel('enable_comments'),
        FieldPanel('tags'),
    ]


    class Meta:
        verbose_name = "Blog Page"


class EventPage(Page):
    """
    Event page with its own content model.

    Independent event page model with event-specific fields and shared content
    functionality. No longer inherits from BlogPage for cleaner separation.

    Attributes
    ----------
    date : DateField
        Publication date of the event announcement
    last_modified : DateTimeField
        Last modification timestamp
    author : ForeignKey
        Reference to Author snippet
    excerpt : TextField
        Short description/summary of the event
    header_image : ImageField
        Featured image for the event
    header_image_alt : CharField
        Alt text for the header image
    body : RichTextField
        Main content describing the event
    enable_comments : BooleanField
        Whether to show comments section
    start_date : DateField
        Date when the event starts/started
    end_date : DateField
        Date when the event ends/ended (optional)
    location : CharField
        Where the event takes place
    event_type : CharField
        Type of event (workshop, webinar, conference, etc.)
    tags : ClusterTaggableManager
        Categories/tags for the event
    """
    date = models.DateField("Post date", help_text="Date when the event was announced")
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        'Author',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='events'
    )
    excerpt = models.TextField(
        blank=True,
        max_length=500,
        help_text="Brief description of the event"
    )
    header_image = models.ImageField(
        upload_to='events/headers/',
        blank=True,
        null=True,
        help_text="Featured image for the event"
    )
    header_image_alt = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alt text for the header image"
    )
    body = RichTextField(blank=True)
    enable_comments = models.BooleanField(
        default=False,
        help_text="Show comments section on this event"
    )
    start_date = models.DateField(
        "Event start date",
        help_text="Date when the event starts"
    )
    end_date = models.DateField(
        "Event end date",
        blank=True,
        null=True,
        help_text="Date when the event ends (optional)"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Where the event takes place"
    )

    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
        ('conference', 'Conference'),
        ('meetup', 'Meetup'),
        ('other', 'Other'),
    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='other',
        help_text="Type of event"
    )

    tags = ClusterTaggableManager(through=EventPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('location'),
        FieldPanel('event_type'),
        FieldPanel('author'),
        FieldPanel('excerpt'),
        FieldPanel('header_image'),
        FieldPanel('header_image_alt'),
        FieldPanel('body'),
        FieldPanel('enable_comments'),
        FieldPanel('tags'),
    ]


    class Meta:
        verbose_name = "Event Page"