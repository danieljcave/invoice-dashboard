from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    """
    Decorator for views that require the user to be a superuser.
    Redirects to login_url if the user is not a superuser.
    """
    decorated_view_func = user_passes_test(lambda u: u.is_superuser, login_url='/')
    return decorated_view_func(view_func)
