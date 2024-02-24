from django.db import models

# Create your models here.
class Welcome(models.Model):
    messageText = models.TextField()

    def updateMessageText(self, newMessageText):
        self.messageText = newMessageText
        self.save()

    def clearMessageText(self):
        self.messageText = ""
        self.save()
