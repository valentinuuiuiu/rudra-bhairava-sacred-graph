from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Listing, Category, ListingImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ListingForm(forms.ModelForm):
    """Form for creating and editing listings."""
    images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'hidden',
            'id': 'id_images',
            'accept': 'image/*'
        }),
        label='Imagini',
        help_text='Poți selecta mai multe imagini. Prima imagine va fi imaginea principală.',
    )
    
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'currency', 'location', 'category', 'subcategory']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
                'placeholder': 'Titlul anunțului'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
                'rows': 6,
                'placeholder': 'Descrie produsul sau serviciul...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'currency': forms.Select(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm'
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
                'placeholder': 'Localitatea'
            }),
            'category': forms.Select(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
                'id': 'id_category'
            }),
            'subcategory': forms.Select(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
                'id': 'id_subcategory'
            }),
        }
        labels = {
            'title': 'Titlu *',
            'description': 'Descriere *',
            'price': 'Preț',
            'currency': 'Monedă',
            'location': 'Locația *',
            'category': 'Categoria *',
            'subcategory': 'Subcategoria',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter categories to only show main categories
        self.fields['category'].queryset = Category.objects.filter(parent__isnull=True)
        self.fields['subcategory'].queryset = Category.objects.all()  # Will be filtered by JS
        self.fields['subcategory'].required = False
        
        # Currency choices
        self.fields['currency'].choices = [
            ('RON', 'Lei (RON)'),
            ('EUR', 'Euro (EUR)'),
            ('USD', 'Dolari (USD)'),
        ]

    def save(self, commit=True):
        listing = super().save(commit=commit)
        if commit:
            images = self.files.getlist('images')
            for idx, image in enumerate(images):
                ListingImage.objects.create(
                    listing=listing,
                    image=image,
                    is_main=(idx == 0),
                    order=idx
                )
        return listing


class CustomUserCreationForm(UserCreationForm):
    """Enhanced user registration form."""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
            'placeholder': 'email@exemplu.com'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
                'placeholder': 'Alege un nume de utilizator'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
            'placeholder': 'Parola ta'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary sm:text-sm',
            'placeholder': 'Confirmă parola'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
