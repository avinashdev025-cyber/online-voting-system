from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import Election, Candidate, Vote
from .forms import VoterRegistrationForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Get basic stats for landing page
    active_elections_count = Election.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
        is_active=True
    ).count()
    
    context = {
        'active_elections_count': active_elections_count,
        'total_voters': User.objects.filter(is_staff=False).count(),
        'total_votes': Vote.objects.count()
    }
    return render(request, 'voting/home.html', context)

def register_voter(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your registration was successful.")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = VoterRegistrationForm()
        
    return render(request, 'voting/register.html', {'form': form})

@login_required
def dashboard(request):
    now = timezone.now()
    # Fetch all active and upcoming elections
    active_elections = Election.objects.filter(is_active=True).order_by('end_date')
    
    # Annotate elections with whether the user has voted
    election_list = []
    for election in active_elections:
        has_voted = Vote.objects.filter(user=request.user, election=election).exists()
        election_list.append({
            'obj': election,
            'has_voted': has_voted,
            'is_ongoing': election.is_ongoing,
            'has_ended': election.has_ended
        })
        
    # Get user's voting history
    voted_elections = Vote.objects.filter(user=request.user).select_related('election', 'candidate').order_by('-timestamp')

    context = {
        'elections': election_list,
        'voted_elections': voted_elections,
        'now': now
    }
    return render(request, 'voting/dashboard.html', context)

@login_required
def election_detail(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    # Check if user has already voted
    has_voted = Vote.objects.filter(user=request.user, election=election).exists()
    
    if has_voted:
        messages.warning(request, "You have already voted in this election.")
        return redirect('results', election_id=election.id)
        
    if election.has_ended:
        messages.info(request, "This election has ended. You can view the results below.")
        return redirect('results', election_id=election.id)
        
    if not election.is_ongoing:
        messages.warning(request, "This election is not currently open for voting.")
        return redirect('dashboard')
        
    candidates = election.candidates.all()
    
    context = {
        'election': election,
        'candidates': candidates,
    }
    return render(request, 'voting/election_detail.html', context)

@login_required
def cast_vote(request, election_id):
    if request.method != 'POST':
        return redirect('election_detail', election_id=election_id)
        
    election = get_object_or_404(Election, pk=election_id)
    candidate_id = request.POST.get('candidate')
    
    if not candidate_id:
        messages.error(request, "Please select a candidate before submitting your vote.")
        return redirect('election_detail', election_id=election_id)
        
    candidate = get_object_or_404(Candidate, pk=candidate_id, election=election)
    
    # Validation checks (Double-voting protection)
    # 1. Check if user already voted in this election
    if Vote.objects.filter(user=request.user, election=election).exists():
        messages.error(request, "Security Alert: You have already cast a vote in this election.")
        return redirect('dashboard')
        
    # 2. Check if election is active and ongoing
    if not election.is_ongoing:
        messages.error(request, "Voting is not allowed as this election is not currently active.")
        return redirect('dashboard')
        
    # Securely save the vote using Django transaction protection (implicit in standard save)
    try:
        vote = Vote(user=request.user, election=election, candidate=candidate)
        vote.save()
        messages.success(request, f"Your vote for '{candidate.name}' has been securely cast!")
    except Exception as e:
        messages.error(request, "An error occurred while saving your vote. Please try again.")
        return redirect('election_detail', election_id=election_id)
        
    return redirect('results', election_id=election.id)

@login_required
def election_results(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = election.candidates.all()
    
    # Fetch results data
    results = []
    total_votes = election.total_votes
    
    for candidate in candidates:
        vote_count = candidate.vote_count
        pct = candidate.get_vote_percentage()
        results.append({
            'name': candidate.name,
            'party': candidate.party_name,
            'votes': vote_count,
            'percentage': pct
        })
        
    # Sort candidates by vote count descending
    results = sorted(results, key=lambda x: x['votes'], reverse=True)
    
    has_voted = Vote.objects.filter(user=request.user, election=election).exists()
    
    context = {
        'election': election,
        'results': results,
        'total_votes': total_votes,
        'has_voted': has_voted
    }
    return render(request, 'voting/results.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Admin stats summary
    total_voters = User.objects.filter(is_staff=False).count()
    total_votes = Vote.objects.count()
    active_elections = Election.objects.filter(is_active=True).order_by('-created_at')
    
    election_summaries = []
    for election in Election.objects.all().order_by('-created_at'):
        candidates = election.candidates.all()
        # Find leading candidate
        leading_candidate = None
        max_votes = -1
        for c in candidates:
            c_votes = c.vote_count
            if c_votes > max_votes:
                max_votes = c_votes
                leading_candidate = c
                
        election_summaries.append({
            'obj': election,
            'total_votes': election.total_votes,
            'is_ongoing': election.is_ongoing,
            'leading_candidate': leading_candidate if max_votes > 0 else None,
            'leading_votes': max_votes if max_votes > 0 else 0
        })
        
    context = {
        'total_voters': total_voters,
        'total_votes': total_votes,
        'active_elections_count': active_elections.count(),
        'election_summaries': election_summaries
    }
    return render(request, 'voting/admin_dashboard.html', context)
