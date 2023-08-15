import django
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  class Meta:
          verbose_name_plural:'Member'
  def __str__(self):
        return self.firstname




class UserProfile(models.Model):
    wallet_address = models.CharField(max_length=42)  # Ethereum wallet address
    challenge = models.CharField(max_length=64, null=True, blank=True)  # Storing the generated challenge hash
    signature = models.CharField(max_length=132, null=True, blank=True)  # Storing the user's signature of the challenge
    access_token = models.CharField(max_length=132, null=True, blank=True)  # Storing the user's signature of the challenge
    challenge_created_at = models.PositiveIntegerField(null=True, blank=True)  # Storing the expiration time of the challenge in Unix timestamp format
    challenge_expiration = models.PositiveIntegerField(null=True, blank=True)  # Storing the expiration time of the challenge in Unix timestamp format
#     challenge_created_at = models.DateTimeField(null=True,blank=True)
    # challenge_expiration = models.DateTimeField(null=True,blank=True)

    
    def __str__(self):
        return self.wallet_address
    

class NFT(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.title