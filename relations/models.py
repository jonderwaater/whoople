from django.db import models
from django.conf import settings

# Create your models here.
class Person(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    first_name     = models.CharField(max_length=50)
    last_name      = models.CharField(max_length=50)
    birth_date     = models.DateField(null=True)
    deceased_date  = models.DateField(null=True)
    gender         = models.CharField(max_length=1,null=True)
    streethouse    = models.CharField(max_length=50,null=True)
    zipcode        = models.CharField(max_length=10,null=True)
    city           = models.CharField(max_length=20,null=True)
    country        = models.CharField(max_length=15,null=True)

    def __str__(self):
        return self.last_name+", "+self.first_name

    class Meta:
        unique_together = [['user','first_name','last_name','birth_date']]

class Parent(models.Model):
    parent          = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='%(class)s_parent')
    child           = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='%(class)s_child')

    def __str__(self):
        return self.parent.first_name+' '+self.parent.last_name

    class Meta:
        unique_together = [['parent','child']]

class Partner(models.Model):
    partner          = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='%(class)s_partner1')
    partner2         = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='%(class)s_partner2')

    def __str__(self):
        return self.partner.first_name+' '+self.partner.last_name

    class Meta:
        unique_together = [['partner','partner2']]

