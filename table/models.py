import uuid
from django.db import models
from main.models import Kitchen
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files import File
from core.settings import DOMAIN as domain


class Table(models.Model):
    # ...

    def generate_qr_code(self):
        # Generate the URL for the kitchen menu with the table number as a parameter
        url = f"{domain}{reverse('main:redirect', args=[self.kitchen.kitchen_id, self.table_unique_id])}"
        
        # Generate QR code for the URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image to the qr_code field
        buffer = BytesIO()
        img.save(buffer)
        filename = f"kitchen_{self.kitchen.id}_table_{self.number}_qr.png"
        self.qr_code.save(filename, File(buffer), save=False)

    TABLE_STATUS_CHOICES = (
        ('available', 'Bo`sh'),
        ('occupied', 'Band'),
        ('reserved', 'Zaxira'),
    )

    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='tables')
    table_unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    number = models.IntegerField()
    capacity = models.IntegerField(default=4)
    views = models.PositiveIntegerField(default=0)
    qr_code = models.ImageField(upload_to='table_qr_codes', blank=True, null=True)
    status = models.CharField(max_length=10, choices=TABLE_STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Table {self.number}"

    def save(self, *args, **kwargs):
        if not self.number:
            last_table = Table.objects.filter(kitchen=self.kitchen).order_by('-number').first()
            if last_table:
                self.number = last_table.number + 1
            else:
                # If there are no tables in the database, start with table number 1
                self.number = 1
        self.generate_qr_code()
        super(Table, self).save(*args, **kwargs)
