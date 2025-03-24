# models.py
from django.db import models



class ExampleModel(models.Model):
    check_in_date = models.CharField(max_length=15, null=True, blank=False)
    check_out_date = models.CharField(max_length=15, null=True, blank=False)
    name = models.CharField(max_length=20, null=True, blank=False)
    furigana = models.CharField(max_length=20, null=True, blank=False)
    people = models.CharField(max_length=3, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    phone_number = models.CharField(max_length=15,null=True, blank=False)
    postal_code = models.CharField(max_length=7,null=True, blank=False)  # 郵便番号用
    address = models.TextField(null=True, blank=False)  # 住所用
    games = models.BooleanField(null=True,blank=True)
    others = models.BooleanField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)  # 初回作成時に自動でセット
    updated_at = models.DateTimeField(null=True, blank=True,auto_now=True) 
   





    



