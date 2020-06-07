from django.db.models.functions import Lower
from django import forms

from .models import Person, Parent, Partner

class PersonForm(forms.ModelForm):
    first_name = forms.CharField(label="first name",required=True)
    last_name = forms.CharField(label="last name",required=False)
    birth_date     = forms.CharField(required=False)
    deceased_date  = forms.CharField(required=False)
    gender         = forms.CharField(required=False)
    streethouse    = forms.CharField(required=False,label="street + number")
    zipcode        = forms.CharField(required=False)
    city           = forms.CharField(required=False)
    country        = forms.CharField(required=False)

    class Meta:
        model = Person
        fields = ('first_name','last_name',)


class ParentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Person.objects.all().order_by(Lower('last_name'),Lower('first_name')), empty_label="(Select)")
    #child = forms.ModelChoiceField(queryset=Person.objects.all(), empty_label="(Nothing)")

    class Meta:
        model = Parent
        fields = ('parent',)#'child',)

class ChildForm(forms.ModelForm):
    child = forms.ModelChoiceField(queryset=Person.objects.all().order_by(Lower('last_name'),Lower('first_name')), empty_label="(Select)")

    class Meta:
        model = Parent
        #fields = ('parent','child',)
        fields = ('child',)

class PartnerForm(forms.ModelForm):
    partner = forms.ModelChoiceField(queryset=Person.objects.all().order_by(Lower('last_name'),Lower('first_name')), empty_label="(Select)")

    class Meta:
        model = Partner
        fields = ('partner',)

