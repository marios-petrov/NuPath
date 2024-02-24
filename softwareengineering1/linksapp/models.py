from django.db import models

# Create your models here.
class Links(models.Model):
    """
    Represents a link object with a title, URL, and an optional description.

    Attributes:
        title (models.CharField): The title of the link.
        url (models.URLField): The URL the link points to.
        description (models.TextField): An optional description for the link; can be blank.
    """

    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        """
        Returns a string representation of the Link object, which is its title.

        Returns:
            str: The title of the link.
        """
        return self.title
