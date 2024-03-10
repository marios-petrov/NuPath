from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    
    # badges
    picked_classes = models.BooleanField(default=False)
    picked_dorm_room = models.BooleanField(default=False)
    checked_ham_menu = models.BooleanField(default=False)
    checked_campus_facilities = models.BooleanField(default=False)
    known_faculty = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Pass along any arguments to the superclass's save.

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
