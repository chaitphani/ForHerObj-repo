from django.shortcuts import redirect
from django.contrib.auth.models import User


def is_authenticated(f):
    def wrap(request, *args, **kwargs):
        # this check the session if userid key exist, if not it will redirect to login page
        try:
            user_obj = User.objects.get(email=request.session['email'])
        except:
            user_obj = False
        if 'email' in request.session.keys() and user_obj:
            return f(request, *args, **kwargs)

        request.session.clear()
        return redirect("/login")
    wrap.__doc__ = f.__doc__
    # wrap.__name__ = f.__name__
    return wrap