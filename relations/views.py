from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.db.models import Q
from django.db import IntegrityError

#from .forms import PersonForm, ParentForm
from .forms import ParentForm, ChildForm, PartnerForm, PersonForm
from .models import Person, Parent, Partner
from whoople.views import PersonView


# Create your views here.
class AddPersonView(CreateView):
    template_name = 'person_edit.html'
    #form_class = PersonForm
    model = Person
    fields = ['first_name','last_name','birth_date','gender','streethouse','zipcode','city','country','deceased_date']
    success_url = '/'

    def get(self, request):
        if request.user.is_authenticated == False :
            return HttpResponse(status=404)
        return super().get(request)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(AddPersonView, self).form_valid(form)


def AddParentView(request, person_id):

    if request.user.is_authenticated == False :
        return HttpResponse(status=404)

    if request.method == "GET":
        form = ParentForm()
        form_newperson = PersonForm()

    if request.method == "POST":
        form = ParentForm(request.POST)
        form_newperson = PersonForm(request.POST)
        if form_newperson.is_valid():
            newperson = form_newperson.save(commit=False)
            newperson.user = request.user
            newperson.save()
            parent = newperson
        if form.is_valid():
            parent = form.cleaned_data['parent']
        parentrel = Parent()
        parentrel.parent = parent
        parentrel.child = Person.objects.get(pk=person_id)
        try:
            parentrel.save()
        except IntegrityError:
            pass
        return redirect('person', person_id=person_id)

    return render(request, 'parent_edit.html', {'form':form,'form_newperson':form_newperson})

def AddChildView(request, person_id):

    if request.user.is_authenticated == False :
        return HttpResponse(status=404)

    if request.method == "GET":
        form = ChildForm()
        form_newperson = PersonForm()

    if request.method == "POST":
        form = ChildForm(request.POST)
        form_newperson = PersonForm(request.POST)
        if form_newperson.is_valid():
            newperson = form_newperson.save(commit=False)
            newperson.user = request.user
            newperson.save()
            child = newperson
        if form.is_valid():
            child = form.cleaned_data['child']
        parentrel = Parent()
        parentrel.parent = Person.objects.get(pk=person_id)
        parentrel.child = child
        try:
            parentrel.save()
        except IntegrityError:
            pass
        return redirect('person', person_id=person_id)


    return render(request, 'parent_edit.html', {'form':form,'form_newperson':form_newperson})

def AddPartnerView(request, person_id):

    if request.user.is_authenticated == False :
        return HttpResponse(status=404)

    if request.method == "GET":
        form = PartnerForm()
        form_newperson = PersonForm()

    if request.method == "POST":
        form = PartnerForm(request.POST)
        form_newperson = PersonForm(request.POST)
        if form_newperson.is_valid():
            newperson = form_newperson.save(commit=False)
            newperson.user = request.user
            newperson.save()
            partner2 = newperson
        if form.is_valid():
            partner2 = form.cleaned_data['partner']
        parentrel = Partner()
        parentrel.partner = Person.objects.get(pk=person_id)
        parentrel.partner2 = partner2
        try:
            parentrel.save()
        except IntegrityError:
            pass
        return redirect('person', person_id=person_id)


    return render(request, 'parent_edit.html', {'form':form,'form_newperson':form_newperson})


def delete_parent(request, person_id, parent_id):
    Parent.objects.get(parent=parent_id, child=person_id).delete()
    return PersonView(request, person_id)

def delete_child(request, person_id, child_id):
    Parent.objects.get(child=child_id, parent=person_id).delete()
    return PersonView(request, person_id)

def delete_partner(request, person_id, partner_id):
    partners = Partner.objects.filter(Q(partner=person_id,partner2=partner_id)|Q(partner=partner_id,partner2=person_id))
    for partner in partners:
        partner.delete()
    return PersonView(request, person_id)


