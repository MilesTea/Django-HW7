from django.contrib import admin

# Register your models here.
from advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
	list_display = ['title', 'description', 'status', 'creator', 'created_at', 'updated_at']
	pass



