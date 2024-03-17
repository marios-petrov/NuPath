from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile  # Ensure you've imported your Profile model

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance automatically whenever a new User instance is created.

    This receiver listens for the `post_save` signal on the User model. When a new User instance
    is saved for the first time (i.e., created), it triggers the creation of an associated Profile
    instance, linking it to the newly created User.

    Args:
        sender (Model): The model class sending the signal (User).
        instance (Model instance): The actual instance of the sender that was saved.
        created (bool): A boolean indicating whether this instance is being created (True)
                        or updated (False).
        **kwargs: Arbitrary keyword arguments.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the associated Profile instance automatically whenever a User instance is saved.

    This receiver listens for the `post_save` signal on the User model. Whenever a User instance
    is saved, regardless of it being a new creation or an update, this signal ensures that the
    associated Profile instance is also saved. This is useful for making sure that changes in the
    User instance that might affect the Profile are automatically propagated.

    Note: This signal does not create a Profile; it assumes the Profile already exists. The creation
    should be handled by `create_user_profile`.

    Args:
        sender (Model): The model class sending the signal (User).
        instance (Model instance): The actual instance of the sender that was saved.
        **kwargs: Arbitrary keyword arguments.
    """
    instance.profile.save()

