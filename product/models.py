from django.db import models
from users.models import Users

# Create your models here.
type_choices = (('csv','csv'), ('xlsx','xslsx'), ('xls','xls'),
                ('pdf','pdf'), ('txt','txt'),('jpeg','jpeg'),('jpg','jpg'))

def location_file(instance, filename):
    return f'users/{instance.user}/{filename}'

class Files_upload(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    up_file = models.FileField(upload_to=location_file, default=False, verbose_name='file')
    data_type = models.CharField(max_length=25, blank=False, choices=type_choices)
    name = models.CharField(max_length=150, default='Undefined')
    favorite = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.up_file}'

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

class Project_List(models.Model):
    project_name = models.CharField(max_length = 50)
    user_name = models.CharField(max_length = 50)
    date = models.DateTimeField(auto_now_add=True)
    # class Meta:
    #     db_table = "dreamreal"

class Project_file_List(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project_name = models.CharField(max_length = 50)
    file_name = models.CharField(max_length = 255)
    file_type = models.CharField(max_length = 10)
    file_path = models.CharField(max_length = 255)
    alfresco_id = models.CharField(max_length = 255)
    file_url = models.CharField(max_length=255)
    processed_file_path = models.CharField(max_length = 255)
    favorite = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)