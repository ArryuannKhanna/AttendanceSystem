from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    joinedClasses = models.JSONField(default=list)
    createdClasses = models.JSONField(default=list)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def add_joined_class(self, class_id):
        if class_id not in self.joinedClasses:
            self.joinedClasses.append(class_id)
            self.save()

    def add_created_class(self, class_id):
        if class_id not in self.createdClasses:
            self.createdClasses.append(class_id)
            self.save()

class Classroom(models.Model):
    hostEmailId = models.CharField(max_length=100, default="")
    code = models.IntegerField(default=1000)
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(CustomUser, related_name='attended_classes')
    attendance_record = models.JSONField(default=[])

class Attendance(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    students = models.ManyToManyField(CustomUser)
