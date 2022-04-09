from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


#! equivalent à models.Manager(status='published')
class PublishedManager(models.Manager):
    def get_queryset(self) :
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Customer(models.Model):

    GENDER_CHOICES=(
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    )

    STATUS_CHOICES=(
        
        ('draft','Draft'),
        ('published','Published'),
        
        )



    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10,choices= GENDER_CHOICES)

    created_by = models.ForeignKey(User,related_name='creatd_by',on_delete=models.PROTECT,default=1)

    created = models.DateTimeField(default=timezone.now)
    
    status = models.CharField(max_length=10,choices= STATUS_CHOICES,default='draft')

    objects = models.Manager()

    published = PublishedManager()


    #! gestion des pluriels
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    

    #! Si on fait customers.str() cela affiche nom + prenom    
    def __str__(self) -> str:
        return "{} {}".format(self.name,self.last_name)

        



    







