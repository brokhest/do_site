from django.db import models

# Create your models here.


class File(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # size = models.IntegerField()
    file = models.FileField(upload_to='')

    def __str__(self):
        return self.name

    def delete(self):
        self.file.delete()
        super().delete()