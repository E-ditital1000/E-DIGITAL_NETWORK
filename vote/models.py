from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid



class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name="Position Title")

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self):
        return self.title

from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    ROLE_CHOICES = (
        ('commissioner', 'Election Commissioner'),
        ('voter', 'Voter'),
        ('observer', 'Observer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    first_name = models.CharField(max_length=30, verbose_name="First Name", null=True, default=None)
    last_name = models.CharField(max_length=30, verbose_name="Last Name",null=True,   default=None)
    university_name = models.CharField(max_length=100, blank=True, null=True)
    high_school_name = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, verbose_name="District")
    county = models.CharField(max_length=50, verbose_name="County")
    citizenship = models.BooleanField(default=False, verbose_name="Has Citizenship")
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(120)], verbose_name="Age", null=True,)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='voter')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"



class Election(models.Model):
    name = models.CharField(max_length=100)
    commissioner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='elections')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_voters = models.IntegerField()
    max_observers = models.IntegerField(default=0)  # New field for maximum number of observers
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Unique identifier
    commissioner_token = models.CharField(default=None, max_length=50, unique=True)  # Commissioner token field

    def __str__(self):
        return self.name

    def has_ended(self):
        return self.end_time < timezone.now()

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if this is a new object being created
        if is_new:
            self.commissioner_token = generate_commissioner_token()  # Generate the token
        super(Election, self).save(*args, **kwargs)  # Call the real save method

def generate_commissioner_token():
    """Generate a unique token for the commissioner."""
    return uuid.uuid4().hex[:8]  # Generates an 8-character long unique identifier


class Notification(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)  # New field to track read status

    def __str__(self):
        return self.message

class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voters', null=True, blank=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='voters')
    voter_id = models.CharField(max_length=50, unique=True)
    can_vote = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.user.username if self.user else "No User", self.election.name)

    @staticmethod
    def create_for_commissioner(election):
        """Creates a voter ID for the commissioner automatically when an election is created."""
        voter_id = str(uuid.uuid4())[:8]  # Generates an 8-character long unique identifier
        voter = Voter(election=election, voter_id=voter_id, can_vote=False)  # Set can_vote to False for commissioner
        voter.save()
        return voter.voter_id

# Adding custom user string representation
def custom_user_str(self):
    return f"{self.profile.first_name} {self.profile.last_name} ({self.username})"

User.add_to_class("__str__", custom_user_str)


class Observer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='observers', null=True, blank=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='observers')
    observer_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{} - {}".format(self.user.username if self.user else "No User", self.election.name)

    
PARTY_CHOICES = (
    ('UP', 'Unity Party'),
    ('LP', 'Liberty Party'),
    ('ANC', 'Alternative National Congress'),
    ('CDC', 'Coalition for Democratic Change'),
    ('PUP', 'People’s Unification Party'),
    ('ALP', 'All Liberian Party'),
    ('MOVEE', 'Movement for Economic Empowerment'),
    ('MDR', 'Movement for Democracy and Reconstruction'),
    ('Rainbow', 'Rainbow Alliance'),
    ('vOLT', 'Vision for Liberia Transformation'),
    ('SUP', 'Students Unification Party'),
    ('PROSA', 'Progressive Student Alliance'),
    ('SIM', 'Mighty Student Integration Movement (SIM)'),
    ('STUD', 'Student Democratic Alliance'),
    # Add more as necessary
)

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates', default=None)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=50)
    about = models.TextField(verbose_name="About the Candidate", blank=True, default="No additional information.")
    total_vote = models.IntegerField(default=0, editable=False)
    party = models.CharField(max_length=50, choices=PARTY_CHOICES, default='Independent')
    image = models.ImageField(verbose_name="Candidate Pic", upload_to='images/')

    def __str__(self):
        return "{} - {}".format(self.name, self.position.title)

    def save(self, *args, **kwargs):
        if self.pk:
            old_image = Candidate.objects.get(pk=self.pk).image
            if self.image != old_image:
                old_image.delete(save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

class ControlVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='control_votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='control_votes')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='control_votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='control_votes')
    party = models.CharField(max_length=50, default='Independent', verbose_name="Party")
    status = models.BooleanField(default=False, verbose_name="Status")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Control Vote"
        verbose_name_plural = "Control Votes"
        unique_together = ('user', 'election', 'position', 'candidate')

    def __str__(self):
        return "{} voted for {} in {} election".format(self.user.username, self.candidate.name, self.election.name)


