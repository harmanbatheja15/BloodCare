from django.db import models

# Create your models here.

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class City(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class BloodBank(models.Model):
    id = models.AutoField(primary_key=True)
    Blood_Bank_Name = models.CharField(max_length=800)
    States = models.CharField(max_length=500)
    City = models.CharField(max_length=500)
    Address = models.CharField(max_length=800)
    Contact_No = models.CharField(max_length=500)

    def __str__(self):
        return self.Blood_Bank_Name
    