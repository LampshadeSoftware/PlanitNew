from django.contrib import admin

# imports the models
from .models import Section, WishList


class SectionAdmin(admin.ModelAdmin):
    list_display = ['crn', 'title', 'course_id', 'section_number']


class WishListAdmin(admin.ModelAdmin):
    list_display = ['subject', 'course_id']


admin.site.register(Section, SectionAdmin)
admin.site.register(WishList, WishListAdmin)
