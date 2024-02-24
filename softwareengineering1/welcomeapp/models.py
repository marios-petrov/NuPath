from django.db import models

# Create your models here.
class Welcome(models.Model):
    """
    Represents a welcome message, allowing for dynamic updates to the message text.
    """
    messageText = models.TextField()

    def updateMessageText(self, newMessageText):
        """
        Updates the welcome message text with a new message.

        Args:
            newMessageText (str): The new message text to replace the current message.
        """
        self.messageText = newMessageText
        self.save()

    def clearMessageText(self):
        """
        Clears the current message text, setting it to an empty string.
        """
        self.messageText = ""
        self.save()
