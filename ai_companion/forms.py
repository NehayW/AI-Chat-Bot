from django.forms import ModelForm
from .models import UserPromptTemplate


class PromptForm(ModelForm):
    class Meta:
        model = UserPromptTemplate
        fields = ["title", "bot_name", "description"]
