from django import forms


class URLForm(forms.Form):
    url_to_analyze = forms.URLField(label='Link do analizy')
