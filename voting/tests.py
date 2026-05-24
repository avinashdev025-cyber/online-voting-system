from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.utils import IntegrityError
from datetime import timedelta
from .models import Election, Candidate, Vote

class VotingSystemTestCase(TestCase):
    def setUp(self):
        # Create a test voter
        self.user = User.objects.create_user(username='testvoter', password='password123')
        
        # Create an active election
        self.active_election = Election.objects.create(
            title="Active Test Election",
            description="Testing active state voting.",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            is_active=True
        )
        
        # Create a closed election
        self.closed_election = Election.objects.create(
            title="Closed Test Election",
            description="Testing closed state voting.",
            start_date=timezone.now() - timedelta(days=5),
            end_date=timezone.now() - timedelta(days=1),
            is_active=True
        )
        
        # Add candidates
        self.candidate1 = Candidate.objects.create(election=self.active_election, name="Candidate A")
        self.candidate2 = Candidate.objects.create(election=self.active_election, name="Candidate B")
        self.closed_candidate = Candidate.objects.create(election=self.closed_election, name="Closed Candidate")

    def test_database_double_voting_prevention(self):
        """Verify that the database layer raises an IntegrityError if a user attempts to vote twice in the same election."""
        # First vote should succeed
        vote1 = Vote.objects.create(user=self.user, election=self.active_election, candidate=self.candidate1)
        self.assertIsNotNone(vote1.id)
        
        # Second vote should trigger IntegrityError due to unique_together constraint
        with self.assertRaises(IntegrityError):
            Vote.objects.create(user=self.user, election=self.active_election, candidate=self.candidate2)

    def test_election_status_helpers(self):
        """Test the properties check for election dates."""
        self.assertTrue(self.active_election.is_ongoing)
        self.assertFalse(self.active_election.has_ended)
        
        self.assertFalse(self.closed_election.is_ongoing)
        self.assertTrue(self.closed_election.has_ended)

    def test_voting_on_closed_election_views(self):
        """Verify that voting on a closed election redirects and sets an error message."""
        self.client.login(username='testvoter', password='password123')
        
        # Post to closed election cast_vote view
        response = self.client.post(f'/election/{self.closed_election.id}/vote/', {'candidate': self.closed_candidate.id}, follow=True)
        
        # Should redirect back to dashboard and have an error message
        self.assertRedirects(response, '/dashboard/')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Voting is not allowed as this election is not currently active.")
        
        # Verify no vote was recorded in database
        self.assertEqual(Vote.objects.filter(election=self.closed_election).count(), 0)

    def test_successful_vote_flow(self):
        """Verify standard user voting flow and subsequent lock out."""
        self.client.login(username='testvoter', password='password123')
        
        # Verify initial results show 0 votes
        self.assertEqual(self.candidate1.vote_count, 0)
        
        # Submit ballot
        response = self.client.post(f'/election/{self.active_election.id}/vote/', {'candidate': self.candidate1.id}, follow=True)
        
        # Should redirect to results page
        self.assertRedirects(response, f'/election/{self.active_election.id}/results/')
        
        # Check that vote was recorded
        self.assertEqual(self.candidate1.vote_count, 1)
        self.assertEqual(self.active_election.total_votes, 1)
        
        # Try to vote again
        response2 = self.client.post(f'/election/{self.active_election.id}/vote/', {'candidate': self.candidate2.id}, follow=True)
        
        # Should redirect to dashboard with warning
        self.assertRedirects(response2, '/dashboard/')
        
        # Check that votes didn't double
        self.assertEqual(self.candidate2.vote_count, 0)
        self.assertEqual(self.active_election.total_votes, 1)
