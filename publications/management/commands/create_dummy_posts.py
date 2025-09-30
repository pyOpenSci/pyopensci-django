from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from publications.models import BlogPage, EventPage, Author
from wagtail.models import Page


class Command(BaseCommand):
    help = "Create dummy blog posts and events for testing pagination and filtering"

    def add_arguments(self, parser):
        parser.add_argument(
            '--blog-posts',
            type=int,
            default=25,
            help='Number of blog posts to create (default: 25)'
        )
        parser.add_argument(
            '--events',
            type=int,
            default=20,
            help='Number of events to create (default: 20)'
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete existing dummy posts before creating new ones'
        )

    def handle(self, *args, **options):
        num_blog_posts = options['blog_posts']
        num_events = options['events']
        delete_existing = options['delete']

        # Get or create a default author
        author, created = Author.objects.get_or_create(
            slug='test-author',
            defaults={
                'name': 'Test Author',
                'bio': 'This is a test author for dummy content.',
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created test author: {author.name}'))

        # Get the home page to use as parent
        home_page = Page.objects.get(depth=2).specific

        # Delete existing dummy posts if requested
        if delete_existing:
            deleted_blogs = BlogPage.objects.filter(title__startswith='Test Blog Post').delete()
            deleted_events = EventPage.objects.filter(title__startswith='Test Event').delete()
            self.stdout.write(self.style.WARNING(
                f'Deleted {deleted_blogs[0]} blog posts and {deleted_events[0]} events'
            ))

        # Create blog posts
        self.stdout.write(self.style.NOTICE(f'\nCreating {num_blog_posts} blog posts...'))
        current_date = timezone.now()

        for i in range(1, num_blog_posts + 1):
            # Distribute posts across multiple years
            year_offset = (i - 1) // 10  # 10 posts per year
            month_offset = (i - 1) % 12
            post_date = current_date - timedelta(days=365 * year_offset + 30 * month_offset)

            blog_post = BlogPage(
                title=f'Test Blog Post {i}',
                slug=f'test-blog-post-{i}',
                date=post_date,
                author=author,
                excerpt=f'This is a test excerpt for blog post {i}. '
                        'It provides a brief overview of the post content.',
                body=f'<p>This is the body content for test blog post {i}.</p>'
                     '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                     'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>',
                enable_comments=True,
            )
            home_page.add_child(instance=blog_post)
            blog_post.save_revision().publish()

            if i % 5 == 0:
                self.stdout.write(f'  Created {i}/{num_blog_posts} blog posts...')

        self.stdout.write(self.style.SUCCESS(f'✓ Created {num_blog_posts} blog posts'))

        # Create events
        self.stdout.write(self.style.NOTICE(f'\nCreating {num_events} events...'))

        event_types = ['workshop', 'webinar', 'conference', 'meetup', 'other']

        for i in range(1, num_events + 1):
            # Mix of past and future events
            if i % 2 == 0:
                # Future event
                event_date = current_date + timedelta(days=30 * i)
            else:
                # Past event
                event_date = current_date - timedelta(days=30 * i)

            event_type = event_types[i % len(event_types)]

            event = EventPage(
                title=f'Test Event {i}',
                slug=f'test-event-{i}',
                date=current_date,
                author=author,
                start_date=event_date.date(),
                end_date=(event_date + timedelta(days=1)).date() if i % 3 == 0 else event_date.date(),
                location='Online' if i % 2 == 0 else 'San Francisco, CA',
                event_type=event_type,
                excerpt=f'This is a test excerpt for event {i}. Join us for this exciting event!',
                body=f'<p>This is the body content for test event {i}.</p>'
                     '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>',
                enable_comments=True,
            )
            home_page.add_child(instance=event)
            event.save_revision().publish()

            if i % 5 == 0:
                self.stdout.write(f'  Created {i}/{num_events} events...')

        self.stdout.write(self.style.SUCCESS(f'✓ Created {num_events} events'))

        # Summary
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Successfully created {num_blog_posts} blog posts and {num_events} events!'
        ))
        self.stdout.write(self.style.NOTICE(
            '\nYou can now test:\n'
            '  - Blog pagination at /blog/ (12 posts per page)\n'
            '  - Events pagination at /events/ (15 events per page)\n'
            '  - Year filtering on blog page\n'
        ))