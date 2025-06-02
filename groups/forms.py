from django import forms
from .models import StudyGroup

class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description', 'subject', 'max_members', 'is_private']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter group name (e.g., "Calculus Study Group")',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your study group, goals, and what members can expect...',
                'rows': 4
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),
            'max_members': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2',
                'max': '50',
                'value': '10'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'name': 'Group Name',
            'description': 'Description',
            'subject': 'Subject Area',
            'max_members': 'Maximum Members',
            'is_private': 'Private Group'
        }
        help_texts = {
            'name': 'Choose a clear, descriptive name for your study group',
            'description': 'Provide details about study goals, meeting frequency, and expectations',
            'subject': 'Select the primary subject area for this group',
            'max_members': 'Set the maximum number of members (2-50)',
            'is_private': 'Private groups require approval to join'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError('Group name must be at least 3 characters long.')
        return name

    def clean_max_members(self):
        max_members = self.cleaned_data.get('max_members')
        if max_members < 2:
            raise forms.ValidationError('A group must have at least 2 members.')
        if max_members > 50:
            raise forms.ValidationError('Maximum group size is 50 members.')
        return max_members
