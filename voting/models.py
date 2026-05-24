from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    @property
    def has_ended(self):
        return timezone.now() > self.end_date or not self.is_active

    @property
    def total_votes(self):
        return self.vote_set.count()

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)
    party_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        if self.party_name:
            return f"{self.name} ({self.party_name})"
        return self.name

    @property
    def vote_count(self):
        return self.vote_set.count()

    def get_vote_percentage(self):
        total = self.election.total_votes
        if total == 0:
            return 0.0
        return round((self.vote_count / total) * 100, 1)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Enforce database-level restriction: one vote per user per election
        unique_together = ('user', 'election')

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name} in {self.election.title}"
