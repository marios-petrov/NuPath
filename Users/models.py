from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from PIL import Image  # Ensure PIL is installed or use `from PIL import Image` if using Pillow

class Profile(models.Model):
    """
    Profile model to extend the default Django User model with a one-to-one relationship.

    This model is designed to store additional information about the user, such as a profile
    picture and various boolean fields to represent badges for completing specific tasks.

    Attributes:
        user (OneToOneField): A one-to-one link to the Django User model. This allows us to add
                              additional information to the user without modifying the User model.
        image (ImageField): An image field to store profile pictures. Defaults to 'default.png' and
                            saves images to the 'profile_pics' directory.
        picked_classes (BooleanField): Indicates whether the user has picked their classes (badge).
        picked_dorm_room (BooleanField): Indicates whether the user has picked a dorm room (badge).
        checked_ham_menu (BooleanField): Indicates whether the user has checked the ham menu (badge).
        checked_campus_facilities (BooleanField): Represents checking campus facilities (badge).
        known_faculty (BooleanField): Indicates whether the user has gotten to know the faculty (badge).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    # Badges
    picked_classes = models.BooleanField(default=False)
    picked_dorm_room = models.BooleanField(default=False)
    checked_ham_menu = models.BooleanField(default=False)
    checked_campus_facilities = models.BooleanField(default=False)
    known_faculty = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the Profile model, showing the related user's username and
        appending 'Profile' to it.

        Returns:
            str: A string indicating whose profile it is.
        """
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to add custom logic for processing the image field.

        When a Profile instance is saved, this method checks the dimensions of the uploaded profile
        picture. If the image's height or width exceeds 300 pixels, it resizes the image to fit
        within a 300x300 box while maintaining aspect ratio.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().save(*args, **kwargs)  # Save the model using the parent class's save method.

        img = Image.open(self.image.path)  # Open the image file of the profile.

        # Resize the image if either dimension is greater than 300 pixels.
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  # Resize the image to fit within the output_size box.
            img.save(self.image.path)  # Save the resized image back to the same path.


