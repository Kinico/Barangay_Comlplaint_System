from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'description', 'location', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your complaint in detail...'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., Block 5, Lot 12, Barangay San Jose'}),
        }