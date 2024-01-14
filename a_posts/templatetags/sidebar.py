from django.template import Library

from ..models import Tag

register = Library()

@register.inclusion_tag('includes/sidebar.html')
def sidebar_view():
    """
    Inclusion tag for rendering the sidebar with a list of all Tag categories.

    This template tag retrieves all Tag objects from the database and includes them in the
    'includes/sidebar.html' template. The list of categories is made available in the
    context dictionary under the key 'categories'.

    Usage in a template:
    {% load your_custom_template_tags %}  <!-- Load the template tags -->
    {% sidebar_view %}  <!-- Include the rendered sidebar in the template -->
    """
    
    categories = Tag.objects.all()
    context = { 'categories' : categories }
    
    return context