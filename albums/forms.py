from typing import Any

from django import forms
from albums.models import Album, Memory


class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['nickname', 'country']
        labels = {
            'nickname': 'Fan Nickname',
            'country': 'Home Country'
        }
        help_texts = {
            'nickname':'Choose a name to display on your BEFAlbum',
            'country': 'The country you are coming from'
        }
        widgets = {
            'nickname': forms.TextInput(attrs={
                'placeholder': 'e.g. BurgasEurovisionFan'
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'e.g. Bulgaria'
            }),
        }

        error_messages = {
            'nickname': {'required': 'Please, enter a nickname for your album!'},
            'country': {'required': 'Please, enter your home country!'},
        }

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '')
        if nickname and len(nickname.strip()) < 3:
            raise forms.ValidationError("Nickname must be at least 3 characters long!")

        return nickname

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class EditAlbumForm(CreateAlbumForm):
    class Meta(CreateAlbumForm.Meta):
        fields = ['nickname', 'country', 'collected_stars']
        labels = {
            **CreateAlbumForm.Meta.labels,
            'collected_stars': 'Total number of collected stars ⭐'
        }
        help_texts = {
            **CreateAlbumForm.Meta.help_texts,
            'collected_stars': 'Automatically calculated from your completed experiences.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collected_stars'].disabled = True


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['note']
        labels = {
            'note': 'Your memory note'
        }
        widgets = {
            'note': forms.Textarea(attrs={
                'placeholder': 'Write a memory ...',
            })
        }