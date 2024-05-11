from django.db import models


class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=25)
    code = models.CharField(max_length=10)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
    
    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"
    
    def verify(self):
        self.verified = True
        self.save()
        return True
    
    def is_verified(self):
        return self.verified
    
    def send(self):
        pass

    