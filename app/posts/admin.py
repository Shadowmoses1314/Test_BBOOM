from django.contrib import admin
from .models import User, Post





@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'body')
    list_display_links = ('id', 'title')
    list_filter = ('user',)  # Add filter by user
    search_fields = ('title', 'body', 'user__name', 'user__email')


admin.site.register(User)
