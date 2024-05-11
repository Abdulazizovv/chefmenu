import random
from users.models import User
from .models import VerificationCode

def is_phone_number_available(phone_number):
    response = User.objects.filter(phone_number=phone_number).first()
    if response:
        return False
    return True


def verification_code_active(phone_number):
    response = VerificationCode.objects.filter(phone_number=phone_number, verified=False)
    if response:
        return True
    return False


def generate_verification_code(phone_number):
    code = ''.join(random.choice('0123456789') for _ in range(6))
    VerificationCode.objects.create(phone_number=phone_number, code=code, verified=False)
    return code


def check_verification_code(phone_number, code):
    verify_code = VerificationCode.objects.filter(phone_number=phone_number, verified=False).first()
    print(verify_code, code)
    if verify_code:
        if verify_code.code == code:
            verify_code.verified = True
            verify_code.save()
            return True
    return False

def get_verification_code(phone_number):
    verify_code = VerificationCode.objects.filter(phone_number=phone_number, verified=False).first()
    if verify_code:
        return verify_code.code
    return None
