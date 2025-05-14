from django import forms
from .models import WebsiteOrderFormRequest, TelegramBotOrderFormRequest

class WebsiteOrderForm(forms.ModelForm):
    class Meta:
        model = WebsiteOrderFormRequest
        fields = ['title', 'description', 'design_type', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 5}),
            'design_type': forms.Select(attrs={'class': 'form-control form-control-lg select-glass'}),
            'price': forms.NumberInput(attrs={
                'type': 'range',
                'class': 'single-slider',
                'min': 1000000,
                'max': 1000000000,
                'step': 100000,
                'value': 5000000,
                'id': 'price-slider'
            }),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'design_type': 'Design Type',
            'price': 'Budget (Toman)',
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        design_type = cleaned_data.get('design_type')

        if price and (price < 1000000 or price > 1000000000):
            self.add_error('price', 'Budget must be between $1,000,000 and $1,000,000,000.')
        if design_type == "Choose an option":
            self.add_error('design_type', 'Please select a design type.')
        return cleaned_data


class TelegramBotOrderForm(forms.ModelForm):
    class Meta:
        model = TelegramBotOrderFormRequest
        fields = ["title", "description", "price"]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            "description": forms.Textarea(attrs={'class': 'form-control form-control-lg', 'row': 5}),
            "price": forms.NumberInput(attrs={
                'type': 'range',
                'class': 'single-slider',
                'min': 1000000,
                'max': 1000000000,
                'step': 100000,
                'value': 5000000,
                'id': 'price-slider'
            }),
        }
        label = {
            'title': 'Title',
            'description': 'Description',
            'price': 'Budget (Toman)',
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        if price and (price < 1000000 or price > 1000000000):
            self.add_error('price', 'Budget must be between 1,000,000 Toman and 1,000,000,000 Toman.')
        return cleaned_data