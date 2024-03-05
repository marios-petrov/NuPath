from django.db import models

# Create your models here.

class Dorms(models.Model):
    #Dorm Choices - look at the Field.choices documentation on Django!
    LETTER = "WXYZV"
    Z = "Z"
    HOME2 = "H2"
    HILTON = "HTN"
    DORTGOLD = "DNG"
    OFFCAMPUS = "OFC"
    DORM_CHOICES = {
        LETTER: "Y, X, W, V",
        Z: "Z",
        HOME2: "Home 2",
        HILTON: "Hilton",
        DORTGOLD: "Dort and Gold",
        OFFCAMPUS: "Off Campus",
    }

    current_dorm = models.CharField( #creates a field on the object for selecting fixed choices
        max_length=1,
        choices=DORM_CHOICES,
        default=LETTER,
    ) #TODO - check if this is needed for the new thing I'm doing
    
    number = models.PositiveIntegerField(editable=True,) #room number
    #food_options = models.CharField(max_length=200) #what food is most available by dorm
    #picture = models.FilePathField.path('foo') #TODO get a file director for the pictures . . . this may want to be a choices field
    #might have to include user id here...?

    #OFFCAMPUS maybe find a way to consolidate this?
    def is_letter(self):
        return self.current_dorm in {self.LETTER}
    
    def is_z(self):
        return self.current_dorm in {self.Z}
    
    def is_hotel(self):
        return self.current_dorm in {self.HOTEL}
    
    def is_dortgold(self):
        return self.current_dorm in {self.DORTGOLD}
    
    def is_offcampus(self):
        return self.current_dorm in {self.OFFCAMPUS}
    
    def room(self):
        return self.number