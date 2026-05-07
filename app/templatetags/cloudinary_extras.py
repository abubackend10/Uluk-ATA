from django import template

register = template.Library()

@register.filter
def optimize_image(url, args=""):
    """
    Appends f_auto,q_auto and additional arguments (like w_600) to Cloudinary URL.
    Usage: {{ object.image.url|optimize_image:"w_600" }}
    """
    if not url or not isinstance(url, str):
        return url
        
    # Check if it's a valid Cloudinary URL
    if '/upload/' in url:
        parts = url.split('/upload/', 1)
        base = parts[0] + '/upload/'
        path = parts[1]
        
        # Base optimization
        transformations = ['f_auto', 'q_auto']
        if args:
            transformations.extend(args.split(','))
            
        transform_str = ','.join(transformations)
        return f"{base}{transform_str}/{path}"
    return url
