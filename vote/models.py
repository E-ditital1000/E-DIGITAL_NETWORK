from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    national_id = models.CharField(max_length=50)
    citizenship = models.BooleanField(default=False)
    age = models.IntegerField()
    residency_proof = models.FileField(upload_to='residency_proofs')

    def __str__(self):
        return self.user.username

class Candidate(models.Model):
    name = models.CharField(max_length=50)
    total_vote = models.IntegerField(default=0, editable=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    district = models.CharField(max_length=50, default='Unknown')
    county = models.CharField(max_length=50, default='Unknown')
    party = models.CharField(max_length=50, default='Unknown')
    image = models.ImageField(verbose_name="Candidate Pic", upload_to='images/')
    
    def __str__(self):
        return "{} - {}".format(self.name, self.position.title)

from django.db import models

class ControlVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    district = models.CharField(max_length=50, default='Unknown')
    county = models.CharField(max_length=50, default='Unknown')
    party = models.CharField(max_length=50, default='Unknown')
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user, self.position, self.district, self.county, self.status)
