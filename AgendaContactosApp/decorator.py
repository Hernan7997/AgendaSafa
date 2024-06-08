# from django.shortcuts import redirect
#
#
from django.shortcuts import redirect


# Decorador para comprobar si el usuario esta logueado
def check_user_logged():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('error')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator

# Decorador para comprobar si el usuario tiene el rol necesario
def check_user_role(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if request.user == "AnonymousUser" or not hasattr(request.user, 'rol') or request.user.rol != required_role:
                return redirect('error')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
