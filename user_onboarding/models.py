from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from cloudinary.models import CloudinaryField 
# Create your models here.



class Roles(models.Model):
    name = models.CharField(max_length=100, null=True)
   
    def __str__(self):
        return self.name

def findObjRole(user_type):
    user_type = Roles.objects.filter(id=user_type).first()
    return user_type

def findIdRole(user_type):
    user_type = Roles.objects.filter(id=user_type).first()
    return user_type.id


class UserManager(BaseUserManager):
    def create_user(self, email, f_name, l_name, user_type, username, password=None, password2=None, profile_photo=None, address=None, city=None, pin=None):
        """
        Creates and saves a User with the given email, name, and username.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            f_name=f_name,
            l_name=l_name,
            username=username,
            user_type=user_type,
            profile_photo=profile_photo,
            address=address,
            city=city,
            pin=pin
        )
        if user_type.id in (1, 2):  # Assuming user_type is an instance of Roles
            user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, f_name, l_name,username, user_type,password=None):
        """
        Creates and saves a superuser with the given email, name, and username number.
        """

        # user = self.create_user(
        #     email=email,
        #     password=password,
        #     f_name=f_name,
        #     l_name=l_name,
        #     username=username,
        #     # user_type=user_type
            
        # )
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            f_name=f_name,
            l_name=l_name,
            username=username,
        )
        user.set_password(password)
        user.user_type = findObjRole(user_type)
        # user.is_admin = True
        if(user.user_type== 1 or 2):
            user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    f_name = models.CharField(max_length=200)
    l_name =  models.CharField(max_length=200)
    username =models.CharField(max_length=200)
    user_type = models.ForeignKey(Roles, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    updated_at =models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)
    profile_photo = CloudinaryField('profile_photo', blank=True, null=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    pin=models.CharField(max_length=6)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",'f_name','l_name','user_type']

    def __str__(self):
        return self.email +'--'+ self.f_name

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