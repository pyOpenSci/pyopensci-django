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
        """
        Return name if available, otherwise GitHub username.
        
        Returns
        -------
        str
            The contributor's display name.
        """
        return self.name or f"@{self.github_username}"
    
    @property
    def github_avatar_url(self) -> Optional[str]:
        """
        Generate GitHub avatar URL from image ID.
        
        Returns
        -------
        str or None
            GitHub avatar URL if image ID exists, None otherwise.
        """
        if self.github_image_id:
            return f"https://avatars.githubusercontent.com/u/{self.github_image_id}?s=400&v=4"
        return None
    
    @property
    def github_profile_url(self) -> str:
        """
        Generate GitHub profile URL.
        
        Returns
        -------
        str
            GitHub profile URL for the contributor.
        """
        return f"https://github.com/{self.github_username}"


class Package(models.Model):
    """
    Django model representing a pyOpenSci package.
    
    This model mirrors the package structure from pyosMeta for future database migration.
    Currently, package data is read directly from YAML files.
    """
    
    # Basic package information
    package_name = models.CharField(max_length=255)
    package_description = models.TextField(null=True, blank=True)
    repository_link = models.URLField(null=True, blank=True)
    version_submitted = models.CharField(max_length=100, null=True, blank=True)
    version_accepted = models.CharField(max_length=100, null=True, blank=True)
    
    # Dates (stored as strings to match YAML format)
    date_accepted = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # URLs and links
    issue_link = models.URLField(null=True, blank=True)
    archive = models.URLField(null=True, blank=True)
    joss = models.URLField(null=True, blank=True)
    
    # Status
    active = models.BooleanField(default=True)
    
    # JSON fields for complex data (SQLite compatible)
    submitting_author = models.JSONField(default=dict, blank=True)
    all_current_maintainers = models.JSONField(default=list, blank=True)
    categories = models.JSONField(default=list, blank=True)
    editor = models.JSONField(default=dict, blank=True)
    eic = models.JSONField(default=dict, blank=True)
    reviewers = models.JSONField(default=list, blank=True)
    partners = models.JSONField(default=list, blank=True)
    labels = models.JSONField(default=list, blank=True)
    gh_meta = models.JSONField(default=dict, blank=True)
    
    # Django metadata
    django_created_at = models.DateTimeField(auto_now_add=True)
    django_updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_accepted', 'package_name']
        verbose_name = "Package"
        verbose_name_plural = "Packages"
        
    def __str__(self) -> str:
        return self.package_name
    
    @property
    def submitting_author_name(self) -> str:
        """
        Get the submitting author's name or GitHub username.
        
        Returns
        -------
        str
            The submitting author's display name.
        """
        author = self.submitting_author or {}
        return author.get('name') or f"@{author.get('github_username', 'Unknown')}"
    
    @property
    def documentation_url(self) -> Optional[str]:
        """
        Get the documentation URL from GitHub metadata.
        
        Returns
        -------
        str or None
            Documentation URL if available, None otherwise.
        """
        return self.gh_meta.get('documentation') if self.gh_meta else None
    