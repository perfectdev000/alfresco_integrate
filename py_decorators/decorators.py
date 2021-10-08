import functools
from django.http import Http404

def check_owner(func: callable):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        pass
    return wrapper
