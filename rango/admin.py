from django.contrib import admin
from .models import Page, Category, UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url']
    exclude = ('first_visit', 'last_visit', 'views')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}


admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
