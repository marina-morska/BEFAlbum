from django import forms
from experiences.models import Experience

class PersonalExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Experience title',
            'description': 'Description',
            'image': 'Image'
        }