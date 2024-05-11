from asgiref.sync import sync_to_async
from verification.utils import get_verification_code


@sync_to_async
def get_verification_code_async(phone_number):
    return get_verification_code(phone_number)