from asgiref.sync import sync_to_async
from botapp.models import BotUsers



@sync_to_async
def add_user(user_id, username, phone_number, first_name, last_name, language_code, is_bot=False):

    if BotUsers.objects.filter(user_id=user_id).exists():
        return None

    user = BotUsers.objects.create(
        user_id=user_id,
        username=username,
        phone_number=phone_number,
        first_name=first_name,
        last_name=last_name,
        language_code=language_code,
        is_bot=is_bot
    )
    return user


@sync_to_async
def check_user_exists(user_id):
    user = BotUsers.objects.filter(user_id=user_id).first()
    if user:
        return user.phone_number
    return False