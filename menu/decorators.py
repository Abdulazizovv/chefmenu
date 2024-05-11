from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

def only_kitchen(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_kitchen:
                if request.user.kitchen.is_active:
                    return view_func(request, *args, **kwargs)
                messages.warning(request, "Diqqat siz to'lovni amalga oshirmagansiz!")
                return redirect('main:index')
        messages.error(request, 'Ruxsat yo`q')
        return redirect('main:index')
    return wrapper