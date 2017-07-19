from django.contrib import admin
from .models import Game, Comment, LoginPassword, Photo

class Game_admin(admin.ModelAdmin):
    list_display = ('title', 'game_type', 'author', 'publication_date', 'price', 'is_accepted')
    list_filter = ('title', 'author', 'game_type', 'publication_date')
    date_hierarchy = 'publication_date'


class Comment_admin(admin.ModelAdmin):
    list_display = ('body', 'user', 'email', 'game', 'created')
    search_fields = ('user', 'game', 'created')
    list_filter = ('user', 'game', 'created')
    date_hierarchy = 'created'


# class LoginPassword_admin(admin.ModelAdmin):
#     list_display = ('body', 'user', 'email', 'game', 'created')
#     search_fields = ('user', 'game', 'created')
#     list_filter = ('user', 'game', 'created')
#     date_hierarchy = 'created'


# class Photo_admin(admin.ModelAdmin):
#     list_display = ('body', 'user', 'email', 'game', 'created')
#     search_fields = ('user', 'game', 'created')
#     list_filter = ('user', 'game', 'created')
#     date_hierarchy = 'created'


admin.site.register(Game, Game_admin)
admin.site.register(Comment, Comment_admin)
admin.site.register(LoginPassword)
admin.site.register(Photo)
