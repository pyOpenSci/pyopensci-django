from django.db import models
from typing import Optional


class Contributor(models.Model):
    """
    Django model representing a pyOpenSci contributor.
    
    This model mirrors the PersonModel from pyosMeta for future database migration.
    Currently, contributor data is read directly from YAML files.
    """
    
    # Basic information
    name = models.CharField(max_length=255, null=True, blank=True)
    github_username = models.CharField(max_length=100, unique=True)
    github_image_id = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    # Dates
    date_added = models.DateField(null=True, blank=True)
    
    # Role flags
    deia_advisory = models.BooleanField(default=False)
    editorial_board = models.BooleanField(default=False)
    emeritus_editor = models.BooleanField(default=False)
    advisory = models.BooleanField(default=False)
    emeritus_advisory = models.BooleanField(default=False)
    board = models.BooleanField(default=False)
    
    # Social media and external links
    twitter = models.CharField(max_length=50, null=True, blank=True)
    mastodon = models.URLField(null=True, blank=True)
    orcidid = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
    # JSON fields for lists (SQLite compatible)
    title = models.JSONField(default=list, blank=True)
    partners = models.JSONField(default=list, blank=True)
    contributor_type = models.JSONField(default=list, blank=True)
    packages_eic = models.JSONField(default=list, blank=True)
    packages_editor = models.JSONField(default=list, blank=True)
    packages_submitted = models.JSONField(default=list, blank=True)
    packages_reviewed = models.JSONField(default=list, blank=True)
    
    # Metadata
    sort = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_added', 'sort', 'name']
        verbose_name = "Contributor"
        verbose_name_plural = "Contributors"
        
    def __str__(self) -> str:
        return self.display_name
    
    @property
    def display_name(self) -> str:
        """Return name if available, otherwise GitHub username."""
        return self.name or f"@{self.github_username}"
    
    @property
    def github_avatar_url(self) -> Optional[str]:
        """Generate GitHub avatar URL from image ID."""
        if self.github_image_id:
            return f"https://avatars.githubusercontent.com/u/{self.github_image_id}?s=400&v=4"
        return None
    
    @property
    def github_profile_url(self) -> str:
        """Generate GitHub profile URL."""
        return f"https://github.com/{self.github_username}"