from django.contrib import admin


# Register your models here.
from .models import ExampleModel
class ExampleModelAdmin(admin.ModelAdmin):
    list_display = (  
        "check_in_date","check_out_date",
        "name", "furigana", "people", "email",
        "phone_number", "postal_code", "address", 'created_at', 'updated_at'
    )

admin.site.register(ExampleModel, ExampleModelAdmin)
