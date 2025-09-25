from django.urls import path
from . import views

from core.views import home_markdown

app_name = 'core'

urlpatterns = [
    path('', home_markdown, name='home'),
    path('blog/', views.blog_index, name='blog_index'),
    path('events/', views.events_index, name='events_index'),
    path('blog/<slug:slug>/', views.serve_blog_page, name='blog_page'),
    path('events/<slug:slug>/', views.serve_event_page, name='event_page'),
]