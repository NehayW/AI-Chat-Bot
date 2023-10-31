from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
import uuid
import os


class ChatGptBot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messageInput = models.TextField()
    bot_response = models.TextField()
    bot_name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserPromptTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prompt")
    title = models.CharField(max_length=200)
    bot_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.user.username + "->" + self.title


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename_start = filename.replace("." + ext, "")
    filename = "%s__%s.%s" % (instance.image_title, filename_start, ext)
    return os.path.join(f"{instance.user.username}", filename)


class UsersGeneratedImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_file_path)
    prompt = models.TextField()
    image_title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.user.username + " " + self.image_title
