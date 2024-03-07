from django.db import models
#from django.urls import reverse

# Create your models here.

class Checklist(models.Model):
    item = models.CharField(max_length=200)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.item

class Dorms(models.Model):
    dormtype = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    #there's a better way to have several images, but i'd prefer to have a fixed three for each dorm. 
    # alternatives later: manytomany....? or charfield storing urls...
    dormpic1 = models.ImageField(upload_to='dormview', blank=True) #THIS ONLY WORKS WITH MEDIA FILE. FOR SOME REASON
    dormpic2 = models.ImageField(upload_to='dormview', blank=True)
    dormpic3 = models.ImageField(upload_to='dormview', blank=True)
    foodoptions = models.CharField(max_length=200)
    
    is_current_dorm = models.BooleanField(default=False) #this should be temporary until user profiles store it
    """
    Talking to myself here so I don't forget, but we should store with the user what dorm they have 
    saved & their dorm number to a profile. We would use a OnetoOne(?) for this. I'm on the fence though, because
    it should be that a User can only pick one dorm, but that one dorm can be selected by many users.
    The dorm number should also be stored in the User profile, but should only be altered by the dorm
    views page. There could be added capability in the profile page, but that should be a later addition.
    """
    
    def __str__(self):
        return self.dormtype
    
    def get_address(self):
        return self.address
    
    def get_foodoptions(self):
        return self.foodoptions
    
    def get_foodoptions_list(self):
        return str(self.foodoptions).split(', ')
    #the str() function is so i don't have to use an entire json processing function
    
    def get_dp1(self):
        return self.dormpic1.url
    
    def get_dp2(self):
        return self.dormpic2.url
    
    def get_dp3(self):
        return self.dormpic3.url


"""
class Dormview(models.Model):
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

    #maybe find a way to consolidate this?
    def is_letter(self):
        return self.current_dorm in {self.LETTER}
    
    def is_z(self):
        return self.current_dorm in {self.Z}
    
    def is_hotel(self):
        return self.current_dorm in {self.HOME2}
    
    def is_dortgold(self):
        return self.current_dorm in {self.DORTGOLD}
    
    def is_offcampus(self):
        return self.current_dorm in {self.OFFCAMPUS}
    
    def room(self):
        return self.number

class Checklist(models.Model):
    item = 
    def __str__:
        return self
"""