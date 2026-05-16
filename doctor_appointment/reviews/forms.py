from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = ['rating', 'review_text']

        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),

            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your experience...'
            }),
        }