from django.db import models

from django.db import models

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    classes_joined = models.ArrayField(models.IntegerField(), default=list)
    classes_created = models.ArrayField(models.IntegerField(), default=list)


class Classroom(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Assuming a many-to-many relationship for students attending the class
    students = models.ArrayField(CustomUser, related_name='joined_classes')
    attendance = models.ArrayField(models.IntegerField(), default=list)

class Attendance(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    students = models.ManyToManyField(CustomUser)



