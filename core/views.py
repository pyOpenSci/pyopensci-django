from django.shortcuts import render


def home(request):
    """Homepage view for PyOpenSci."""
    context = {
        'page_title': 'Welcome to pyOpenSci',
        'hero_title': 'We make it easier for scientists to create, find, maintain, and contribute to reusable code and software.',
        'hero_subtitle': 'pyOpenSci broadens participation in scientific open source by breaking down social and technical barriers. Join our global community.',
    }
    return render(request, 'core/home.html', context)