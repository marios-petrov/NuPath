from django.db import models

# Create your models here.
class Notes(models.Model):
    noteText = models.TextField()

    def updateNoteText(self, newNoteText):
        self.noteText = newNoteText
        self.save()

    def clearNoteText(self):
        self.noteText = ""
        self.save()
