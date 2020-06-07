from django.urls import path
from .views import AddPersonView, AddParentView, AddChildView, AddPartnerView, delete_parent, delete_child, delete_partner

app_name='relations'
urlpatterns = [
    path('relations/addperson', AddPersonView.as_view(), name='addperson'),
    #path('relations/addparent', AddParentView.as_view(), name='addparent'),
    path('relations/<int:person_id>/addparent', AddParentView, name='addparent'),
    path('relations/<int:person_id>/addchild', AddChildView, name='addchild'),
    path('relations/<int:person_id>/addpartner', AddPartnerView, name='addpartner'),
    path('relations/<int:person_id>/deleteparent/<int:parent_id>', delete_parent, name='deleteparent'),
    path('relations/<int:person_id>/deletechild/<int:child_id>', delete_child, name='deletechild'),
    path('relations/<int:person_id>/deletepartner/<int:partner_id>', delete_partner, name='deletepartner'),
    ]
