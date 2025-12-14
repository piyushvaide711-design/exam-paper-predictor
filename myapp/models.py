from django.db import models

# Create your models here.

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    semester = models.IntegerField()
    csv_filename = models.CharField(max_length=100, default='unknown.csv')
    # Optional: add college later
    # college = models.CharField(max_length=100, null=True, blank=True)


class UploadedPaper(models.Model):
    # college = models.CharField(max_length=100)
    # semester = models.IntegerField()
    # subject = models.CharField(max_length=200)
    # file = models.FileField(upload_to="question_papers/")
    paper = models.FileField(upload_to='uploaded_papers/',  null=True,
    blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

