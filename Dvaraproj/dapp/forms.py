
from django import forms
from .models import Person, Subcategory

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'category', 'subcategory')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                country_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.country.city_set.order_by('name')