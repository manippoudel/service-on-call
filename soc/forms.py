from django import forms
from .models import  (
    Service_Provider,
    Review,
)

#add sp form

class  SPForm(forms.ModelForm):
    class Meta():
        model = Service_Provider
        fields = ('name', 'panno', 'location', 'about', 'image', 'contactno')
        
class ReviewForm(forms.ModelForm):
    class Meta():
         model = Review 
         fields = ('comment', 'rating')
