#Author Nate Clark

from django.db import models

# Create your models here.
class Notes(models.Model):
    """
    Represents a note.

    Attributes:
        noteText (str): The text of the note.
    """

    noteText = models.TextField()

    def updateNoteText(self, newNoteText):
        """
        Updates the note text with the given new text.

        Args:
            newNoteText (str): The new text for the note.
        """
        self.noteText = newNoteText
        self.save()

    def clearNoteText(self):
        """
        Clears the note text.
        """
        self.noteText = ""
        self.save()
