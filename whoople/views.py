from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import render, redirect
from django.urls import reverse

from relations.models import Person, Parent, Partner

class Home(TemplateView):
    template_name = 'home.html'
    #context_object_name = 'hello'

    def get(self, request):
        if self.request.user.id == None:
            return redirect('account_login')
        return super(Home, self).get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persons'] = queryset=Person.objects.filter(user=self.request.user).order_by(Lower('last_name'),Lower('first_name'))
        return context

class PersonUpdate(UpdateView):
    model = Person
    fields = ['first_name','last_name','birth_date','gender','streethouse','zipcode','city','country','deceased_date']
    template_name= 'person_update_form.html'

    def get_form(self, form_class=None):
        form = super(PersonUpdate, self).get_form(form_class)
        form.fields['birth_date'].required = False
        form.fields['gender'].required = False
        form.fields['streethouse'].required = False
        form.fields['zipcode'].required = False
        form.fields['city'].required = False
        form.fields['country'].required = False
        form.fields['deceased_date'].required = False
        form.fields['last_name'].required = False
        form.fields['streethouse'].label = 'Street + number'
        return form

    def get_object(self, queryset=None):
        obj = Person.objects.get(pk=self.kwargs['person_id'])
        return obj

    def get_success_url(self):
        person_id = self.kwargs['person_id']
        return reverse('person',kwargs={'person_id':person_id})


def PersonView(request, person_id):
    person = Person.objects.get(pk=person_id)
    children = Person.objects.filter(parent_child__in=Parent.objects.filter(parent=person))
    parents = Person.objects.filter(parent_parent__in=Parent.objects.filter(child=person))
    partners = Person.objects.filter(Q(partner_partner2__in=Partner.objects.filter(partner=person))|Q(partner_partner1__in=Partner.objects.filter(partner2=person)))

    siblings = Person.objects.none()
    for parent in parents:
        siblings = siblings | Person.objects.filter(parent_child__in=Parent.objects.filter(parent=parent))
    siblings = siblings.distinct().exclude(pk=person.pk)


    return render(request, 'person.html', {'person':person,'partners':partners,'parents':parents,'children':children,'siblings':siblings})

def delete_person(request, person_id):
    Person.objects.get(pk=person_id).delete()
    return redirect('home')
