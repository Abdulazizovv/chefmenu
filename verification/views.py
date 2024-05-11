import json
from django.http import JsonResponse
from django.shortcuts import render
from .utils import is_phone_number_available, verification_code_active, generate_verification_code
from .models import VerificationCode


def index(request):
    if request.method == "POST":
        body = json.loads(request.body)
        phone_number = body['phone_number']
        if is_phone_number_available(phone_number):
            if verification_code_active(phone_number):
                pass
            else:
                code = generate_verification_code(phone_number)
        return JsonResponse({"message": "Hello, World!"})