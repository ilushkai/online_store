from django import forms

from blog.models import Material

forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

class BlogForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = ('title', 'content', 'image')

    def clean_title(self):
        cleaned_data = self.cleaned_data['title']
        if cleaned_data in forbidden_words:
            raise forms.ValidationError('В названии есть запрещенные слова')
        return cleaned_data

    def clean_content(self):
        cleaned_data = self.cleaned_data['content']
        if cleaned_data in forbidden_words:
            raise forms.ValidationError('В описании есть запрещенные слова')
        return cleaned_data

