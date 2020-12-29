from django.db import models

# Create your models here.

class Account(models.Model):
	iban = models.TextField()
	balance = models.IntegerField()
