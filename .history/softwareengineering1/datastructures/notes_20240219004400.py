from django.db import models
class Notes(models.Model):
    noteText = models.TextField()

    def updateNoteText(self, newNoteText):
        self.noteText = newNoteText
        self.save()

    def clearNoteText(self):
        self.noteText = ""
        self.save()
