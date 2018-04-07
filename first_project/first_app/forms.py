from django import forms
from first_app.models import Query

class QueryForm(forms.ModelForm):
    class Meta():
        model = Query
        fields = '__all__'
