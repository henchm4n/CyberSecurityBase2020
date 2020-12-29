from django.db import models

from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

class File(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	data = models.FileField(upload_to=user_directory_path)
