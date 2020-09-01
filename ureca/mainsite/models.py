from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Corse(models.Model):
    id=models.AutoField(primary_key=True)
    corse_code=models.CharField(max_length=15,default='')
    corse_desc=models.CharField(max_length=300,default='')
    corse_name=models.CharField(max_length=50,default='')
    corse_available=models.CharField(max_length=50,default='')
    corse_instructor_1=models.CharField(max_length=50,default='')
    corse_instructor_2=models.CharField(max_length=50,default='')
    imag_1=models.ImageField(upload_to="mainsite/images",default="")
    imag_2=models.ImageField(upload_to="mainsite/images",default="")

    def __str__(self):
        return self.corse_code

class Modules(models.Model):
    m_id=models.AutoField(primary_key=True)
    code=models.CharField(max_length=15,default='')
    desc=models.CharField(max_length=300,default='')
    name=models.CharField(max_length=50,default='')
    available=models.CharField(max_length=50,default='')
    instructor_1=models.CharField(max_length=50,default='')
    instructor_2=models.CharField(max_length=50,default='')
    imag1=models.ImageField(upload_to="mainsite/images",default="")
    imag2=models.ImageField(upload_to="mainsite/images",default="")
    slug=models.CharField(max_length=130)

    def __str__(self):
        return self.code

class CourseComment(models.Model):
    m_id=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(Modules,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)
    

    def __str__(self):
        return self.comment[0:3]+'...'+"by"+self.user.email


class Rating(models.Model):
    m_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField()
    def __str__(self):
        return self.m_id


class Rating2(models.Model):
    m_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField()
    course=models.ForeignKey(Modules,on_delete=models.CASCADE)
    def __str__(self):
        return self.m_id

class Rating3(models.Model):
    m_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField()
    course=models.ForeignKey(Modules,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.rating)+' by '+self.user.email

    