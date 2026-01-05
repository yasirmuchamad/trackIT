def menu_context(request):
    """Context processor to help with menu active states"""
    
    context = {
        'current_app': None,
        'current_url_name': None,
    }
    
    if hasattr(request, 'resolver_match') and request.resolver_match:
        context['current_app'] = request.resolver_match.app_name
        context['current_url_name'] = request.resolver_match.url_name
    
    return context