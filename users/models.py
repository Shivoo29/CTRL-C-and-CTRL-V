from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
# custom user manager 
class UserManager(BaseUserManager):
    def create_user(self, email,name,phn,password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phn = phn
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,name,phn, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name= name,
            phn= phn,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# custom user model 
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    phn = models.IntegerField(default=1234)
    is_admin = models.BooleanField(default=False)
    # to do may add bank details like ac no etc
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","phn",]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Report(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image_1 = models.ImageField(upload_to='report_images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='report_images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='report_images/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='report_images/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='report_images/', null=True, blank=True)
    image_6 = models.ImageField(upload_to='report_images/', null=True, blank=True)

    def __str__(self):
        return f"Reports :{self.title}"




class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.latitude}, {self.longitude}"