from django.contrib import admin
from .models import ExampleModel

@admin.register(ExampleModel)
class ExampleModelAdmin(admin.ModelAdmin):
    list_display = ('check_in_date', 'check_out_date', 'name','furigana', 'men', 'women', 'yakiniku', 'games', 'others','messages','phone_number','address','email')  # 修正


