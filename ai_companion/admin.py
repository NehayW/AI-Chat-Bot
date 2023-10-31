from django.contrib import admin
from .models import ChatGptBot, UserPromptTemplate, UsersGeneratedImages

admin.site.register(ChatGptBot)
admin.site.register(UsersGeneratedImages)


class PromptAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "bot_name")
admin.site.register(UserPromptTemplate, PromptAdmin)

