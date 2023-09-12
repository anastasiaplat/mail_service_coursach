from django.contrib import admin

# Register your models here.
from .models import Letter, Profile
admin.site.register(Letter)

class ProfileAdmin(admin.ModelAdmin):
    list=['user', 'image', 'date_of_birth']
admin.site.register(Profile, ProfileAdmin)