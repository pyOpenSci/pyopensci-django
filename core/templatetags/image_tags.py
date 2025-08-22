from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def responsive_image(image_path, alt_text="", css_classes="", sizes="100vw"):
    """
    Generate a responsive picture element with WebP and PNG fallback.
    
    Parameters
    ----------
    image_path : str
        Path to the image without extension (e.g., 'headers/pyopensci-sprints').
    alt_text : str, default ""
        Alt text for accessibility.
    css_classes : str, default ""
        CSS classes to apply to the img element.
    sizes : str, default "100vw"
        Sizes attribute for responsive images.
    
    Returns
    -------
    str
        HTML picture element with WebP and PNG fallback.
    """
    webp_path = static(f"images/{image_path}.webp")
    png_path = static(f"images/{image_path}.png")
    
    picture_html = f"""
    <picture>
        <source srcset="{webp_path}" type="image/webp">
        <img src="{png_path}" alt="{alt_text}" class="{css_classes}" loading="lazy" sizes="{sizes}">
    </picture>
    """
    
    return mark_safe(picture_html.strip())


@register.simple_tag
def hero_image(image_path, alt_text=""):
    """
    Generate a hero image with WebP support and optimized loading.
    
    Parameters
    ----------
    image_path : str
        Path to the image without extension.
    alt_text : str, default ""
        Alt text for accessibility.
    
    Returns
    -------
    str
        HTML picture element optimized for hero sections.
    """
    return responsive_image(
        image_path=image_path,
        alt_text=alt_text,
        css_classes="w-full h-full object-cover absolute inset-0",
        sizes="100vw"
    )


@register.simple_tag
def card_image(image_path, alt_text=""):
    """
    Generate a card image with WebP support.
    
    Parameters
    ----------
    image_path : str
        Path to the image without extension.
    alt_text : str, default ""
        Alt text for accessibility.
    
    Returns
    -------
    str
        HTML picture element optimized for card layouts.
    """
    return responsive_image(
        image_path=image_path,
        alt_text=alt_text,
        css_classes="w-full h-full object-cover",
        sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
    )