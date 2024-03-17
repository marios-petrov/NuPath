from django import forms
from .models import *

class AddCalendarEvent(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'description', 'start_time']


from django import forms
from .models import Post  # Make sure to import your Post model


class PostForm(forms.ModelForm):
    """
    A Django form for creating and updating Post objects.

    This form is linked to the Post model and includes fields for the post's title and content.
    It leverages Django's ModelForm capabilities to automatically generate form fields that
    correspond to the model fields, ensuring that data validation and form rendering are
    consistent with the model's definitions.

    Attributes:
        model (Model): The Django model to which this form is linked, which is the Post model in this case.
        fields (list): A list specifying the model fields that should be included in the form.
                       Here, it includes 'title' and 'content' fields of the Post model.
    """

    class Meta:
        model = Post  # Specifies the Django model to create or update
        fields = ['title', 'content']  # Specifies the fields to include in the form
