


def authenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return 
        return wrapper
    return authenticated_user