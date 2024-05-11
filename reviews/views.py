import logging
from django.shortcuts import redirect, render, get_object_or_404
from menu.decorators import only_kitchen
from users.models import Kitchen, User
from .models import ReviewKitchen
from django.contrib import messages


def review_kitchen(request, kitchen_id):
    kitchen = get_object_or_404(Kitchen, id=kitchen_id)
    comments = ReviewKitchen.objects.filter(kitchen=kitchen).order_by("-created")
    if request.method == "POST":
        if request.user.is_authenticated:
            text = request.POST.get("post_body")
            user = request.user
            try:
                comment = ReviewKitchen.objects.create(
                    kitchen=kitchen,
                    user=user,
                    body=text
                )
                comment.save()
                messages.success(request, "Sharh yuborildi!")
            except Exception as err:
                logging.error(err)
                messages.error(request, "Nimadir xato ketdi!...")
            return redirect("review:kitchen", kitchen.id)
    context = {
        "comments": comments,
        "kitchen": kitchen,
    }
    return render(request, "main/review_kitchen.html", context=context)

@only_kitchen
def kitchen_comment_manage(request):
    comments = ReviewKitchen.objects.filter(kitchen=request.user.kitchen).order_by("-created")
    if request.method == "POST":
        comment_id = request.POST.get("comment_id" or None)
        action = request.POST.get("action" or None)
        # comment = get_object_or_404(ReviewKitchen, id=comment_id)
        if action == "delete":
            # comment.delete()
            messages.success(request, "Sharh o'chirildi!")
        elif action =="reply":
            print(request.POST)
        return redirect("review:kitchen_comment_manage")
    context = {
        "comments": comments,
    }
    return render(request, "kitchen/kitchen_comment_manage.html", context=context)