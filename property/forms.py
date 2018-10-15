from django import forms
from django.forms import inlineformset_factory
from django.forms.models import modelformset_factory
from .models import Property





class PropertyForm(forms.ModelForm):

    tags = forms.CharField(label='Related tags', required=False)

    class Meta:
        model = Property

        fields = (
            'title',
            'description',
            'address',
            'neighborhood',
            'storey',
            'category',
            'city',
            'bedroom',
            'bathroom',
            'furnished',
            'parking_space',
            'address',
            'new_property',
            'purpose',
            'square_meter',
            'price',
            'main_image',
            "main_image_two",
            
        )
        widgets = {
            'description' : forms.Textarea(
                attrs= {
                    'placeholder': 'description'
                }
            ) 
        }



