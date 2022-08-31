from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from blood_donation_app.models import State, City

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, name, email, phone, blood_group, state, city, donate_plasma, password=None):
        if not email:
            raise ValueError("Users must have an email address!")
        user = self.model(
            name = name,
            email = self.normalize_email(email),
            phone = phone,
            state = state,
            city = city,
            blood_group = blood_group,
            donate_plasma = donate_plasma,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, phone, blood_group, name, state, city, donate_plasma):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            name = name,
            phone = phone,
            state = state,
            city = city,
            blood_group = blood_group,
            donate_plasma = donate_plasma,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):

    blood_group_choices = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )

    plasma_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    id = models.AutoField(primary_key=True)
    username = None
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=100, unique=False)
    blood_group = models.CharField(choices=blood_group_choices, max_length=250)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    donate_plasma = models.CharField(choices=plasma_choices, max_length=250, default="No")
    
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name', 'blood_group', 'state', 'city', 'donate_plasma']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
