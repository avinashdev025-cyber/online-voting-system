import os
import django
from django.utils import timezone
from datetime import timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_system.settings')
django.setup()

from django.contrib.auth.models import User
from voting.models import Election, Candidate, Vote

def seed_database():
    print("Seeding database...")

    # 1. Create Superuser (Admin)
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminsecure123')
        print("Created superuser: admin (password: adminsecure123)")
    else:
        print("Superuser admin already exists.")

    # 2. Create Test Voters
    voter1, created1 = User.objects.get_or_create(username='voter1')
    if created1:
        voter1.set_password('voter1secure')
        voter1.first_name = "Avinash"
        voter1.last_name = "Sah"
        voter1.email = "voter1@example.com"
        voter1.save()
        print("Created voter: voter1 (password: voter1secure)")

    voter2, created2 = User.objects.get_or_create(username='voter2')
    if created2:
        voter2.set_password('voter2secure')
        voter2.first_name = "Priya"
        voter2.last_name = "Sharma"
        voter2.email = "voter2@example.com"
        voter2.save()
        print("Created voter: voter2 (password: voter2secure)")

    # 3. Create active voters for seed voting
    additional_voters = []
    for i in range(3, 15):
        uname = f'voter{i}'
        v, created = User.objects.get_or_create(username=uname)
        if created:
            v.set_password('votersecure123')
            v.save()
        additional_voters.append(v)

    # 4. Create Ongoing Election
    now = timezone.now()
    general_election, created_gen = Election.objects.get_or_create(
        title="General Election 2026",
        defaults={
            'description': "National election to select legislative representatives. All citizens are eligible to cast their single vote. Results will be calculated and finalized at the end date.",
            'start_date': now - timedelta(days=1),
            'end_date': now + timedelta(days=5),
            'is_active': True
        }
    )
    if created_gen:
        print("Created ongoing election: General Election 2026")
        # Add candidates
        c1 = Candidate.objects.create(
            election=general_election,
            name="Aarav Sharma",
            party_name="Democratic Front",
            bio="Promising clean energy transition, educational upgrades, and digital economy funding."
        )
        c2 = Candidate.objects.create(
            election=general_election,
            name="Neha Patel",
            party_name="National Unity Party",
            bio="Focusing on infrastructure development, small business tax credits, and community health centers."
        )
        c3 = Candidate.objects.create(
            election=general_election,
            name="Rajesh Iyer",
            party_name="Progressive Alliance",
            bio="Advocating for public transit expansion, carbon taxes, and universal state healthcare programs."
        )
        print("Added candidates to General Election 2026")

        # Cast a few votes for demo (e.g. 5 votes)
        Vote.objects.create(user=additional_voters[0], election=general_election, candidate=c1)
        Vote.objects.create(user=additional_voters[1], election=general_election, candidate=c2)
        Vote.objects.create(user=additional_voters[2], election=general_election, candidate=c1)
        Vote.objects.create(user=additional_voters[3], election=general_election, candidate=c3)
        Vote.objects.create(user=additional_voters[4], election=general_election, candidate=c2)
        print("Casted active votes to General Election 2026")

    # 5. Create Ended Election
    student_election, created_stud = Election.objects.get_or_create(
        title="Student Council Election 2025",
        defaults={
            'description': "Annual selection of the Student Council President. This poll has closed and its results are finalized.",
            'start_date': now - timedelta(days=10),
            'end_date': now - timedelta(days=1),
            'is_active': True
        }
    )
    if created_stud:
        print("Created closed election: Student Council Election 2025")
        # Add candidates
        sc1 = Candidate.objects.create(
            election=student_election,
            name="Pooja Roy",
            party_name="Youth Spark",
            bio="Advocating for better sports equipment, common room expansion, and extended library timings."
        )
        sc2 = Candidate.objects.create(
            election=student_election,
            name="Amit Singh",
            party_name="Students First",
            bio="Pledging healthy options in the cafeteria, internship pairing events, and faster campus Wi-Fi."
        )
        print("Added candidates to Student Council Election 2025")

        # Seed votes for this election (voter1, voter2 and additional voters)
        Vote.objects.create(user=voter1, election=student_election, candidate=sc1)
        Vote.objects.create(user=voter2, election=student_election, candidate=sc2)
        
        # Additional votes
        import random
        candidates = [sc1, sc2]
        # Cast votes for other voters
        for idx, v in enumerate(additional_voters):
            # Alternate votes to make it interesting
            cand = candidates[idx % 2]
            Vote.objects.create(user=v, election=student_election, candidate=cand)
            
        print("Casted historical votes to Student Council Election 2025")

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
