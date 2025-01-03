# models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_email(value):
   if 'gmail.com' in value:
       return value
   elif 'yahoo.co.jp' in value:
       return value
   elif 'icloud.com' in value:
       return value
   elif 'yahoo.com' in value:
       return value
   else:
       raise ValidationError("アドレスは有効ではありません。")

MEMBERS = [
   ('1', '1人'),('2', '2人'), ('3', '3人'), ('4', '4人'), ('5', '5人'), ('6', '6人')
]
class ExampleModel(models.Model):
    check_in_date = models.CharField(max_length=15, null=True, blank=True)
    check_out_date = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    furigana = models.CharField(max_length=20, null=True, blank=True)
    people = models.CharField(max_length=3, choices=MEMBERS, null=True, blank=True,)
    email = models.EmailField(validators=[validate_email], null=True, blank=True, help_text="gmail,yahoo,icloudのみ有効")
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    postal_code = models.CharField(max_length=7,null=True, blank=True)  # 郵便番号用
    address = models.TextField(null=True, blank=True)  # 住所用
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)  # 初回作成時に自動でセット
    updated_at = models.DateTimeField(null=True, blank=True,auto_now=True) 
    def __str__(self):
        return self.name


    



