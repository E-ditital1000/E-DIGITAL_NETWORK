from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import (RegistrationForm, LoginForm, ChangePasswordForm, EditProfileForm,
                    ElectionForm, VoterForm, CandidateForm, ControlVoteForm)
from .models import Profile, Election, Voter, Candidate, ControlVote, Position
import uuid
from django.db.models import Q
from django.contrib import messages

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from vote.models import Profile


def homeView(request):
    return render(request, 'vote/home.html')

def terms_of_service(request):
    return render(request, 'vote/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'vote/privacy_policy.html')


def registrationView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            if profile.role == 'voter':
                voter_id = form.cleaned_data.get('voter_id')
                try:
                    voter = Voter.objects.get(voter_id=voter_id, user__isnull=True)
                    voter.user = user
                    voter.save()
                    login(request, user)
                    messages.success(request, "Registration successful.")
                    return redirect('dashboard')
                except Voter.DoesNotExist:
                    user.delete()  # Cleanup the user if voter_id is invalid
                    messages.error(request, "Invalid or already used Voter ID.")
            elif profile.role == 'commissioner':
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()
    
    return render(request, 'vote/register.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'vote/login.html', {'form': form})

def logoutView(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')

@login_required
def dashboardView(request):
    return render(request, 'vote/dashboard.html')

@login_required
def changePasswordView(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            login(request, request.user)  # Re-login the user
            messages.success(request, "Password changed successfully.")
            return redirect('dashboard')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'vote/change_password.html', {'form': form})

@login_required
def editProfileView(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'vote/edit_profile.html', {'form': form})
@login_required
def positionView(request):
    positions = Position.objects.all()
    return render(request, 'vote/positions.html', {'positions': positions})

@login_required
def candidateView(request, pos):
    candidates = Candidate.objects.filter(position_id=pos)
    return render(request, 'vote/candidates.html', {'candidates': candidates})

@login_required
def candidateDetailView(request, id):
    candidate = Candidate.objects.get(id=id)
    return render(request, 'vote/candidate_detail.html', {'candidate': candidate})

@login_required
def resultView(request):
    results = ControlVote.objects.all()
    return render(request, 'vote/results.html', {'results': results})

def commissioner_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if profile.role != 'commissioner':
            return HttpResponseForbidden("Unauthorized.")
        return view_func(request, *args, **kwargs)
    return wrapper_func

from django.core.mail import send_mail
from django.conf import settings

import logging
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

logger = logging.getLogger(__name__)

@login_required
def createElectionView(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            election.commissioner = request.user
            election.commissioner_token = uuid.uuid4()  # Generate a new UUID for the commissioner_token
            election.save()

            # Create a voter ID for the commissioner (if this is required logic)
            voter_id = Voter().create_for_commissioner(election)

            messages.success(request, "Election created successfully. Please Check your Email!")

            # Prepare email context
            context = {
                'commissioner_name': request.user.get_full_name(),
                'election_name': election.name,
                'election_id': election.pk,
                'voter_id': voter_id,
                'commissioner_token': election.commissioner_token,  # Add commissioner_token to the context
                'election_details_url': f"{request.scheme}://{request.get_host()}/election/{election.pk}/",
                'contact_url': f"{request.scheme}://{request.get_host()}/contact/",
                'unsubscribe_url': f"{request.scheme}://{request.get_host()}/unsubscribe/",
                'privacy_policy_url': f"{request.scheme}://{request.get_host()}/privacy-policy/",
            }

            # Render the HTML email template
            html_content = render_to_string('email_templates/new_election_voter_id.html', context)
            text_content = strip_tags(html_content)

            try:
                # Send the HTML email
                email = EmailMultiAlternatives(
                    'New Election and Voter ID',
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [request.user.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
            except Exception as e:
                logger.error(f"Failed to send email to {request.user.email}: {e}")
                messages.error(request, "Failed to send email.")

            return redirect('dashboard')
    else:
        form = ElectionForm()
    return render(request, 'vote/create_election.html', {'form': form})






@login_required
@commissioner_only
def createCandidateView(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election
            candidate.save()
            messages.success(request, "Candidate added successfully.")
            return redirect('election_detail', election_id=election_id)  # Use election_id instead of pk
    else:
        form = CandidateForm(initial={'election': election})
    return render(request, 'vote/create_candidate.html', {'form': form, 'election': election})


import uuid

def generate_unique_voter_id():
    return str(uuid.uuid4())[:8]  # Generates an 8-character long unique identifier

@login_required
def registerVoterView(request, election_id):
    election = get_object_or_404(Election, pk=election_id, commissioner=request.user)

    if request.method == 'POST':
        form = VoterForm(request.POST, user=request.user)
        if form.is_valid():
            if election.voters.count() < election.max_voters:
                voter_id = generate_unique_voter_id()
                voter = form.save(commit=False)
                voter.election = election
                voter.voter_id = voter_id
                voter.save()

                # Prepare and send the email
                context = {
                    'voter_id': voter.voter_id,
                    'election_name': election.name
                }
                html_content = render_to_string('email_templates/new_voter_id.html', context)
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    'New Voter ID Generated',
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [election.commissioner.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)

                messages.success(request, "Voter registered successfully.")
                return redirect('election_detail', election_id=election.id)
            else:
                messages.error(request, "Maximum number of voters reached for this election. You cannot register more voters.")
        else:
            messages.error(request, "Form is not valid. Please correct the errors.")
    else:
        form = VoterForm(user=request.user)  # Create form with user parameter, no need for request.POST

    return render(request, 'vote/register_voter.html', {'form': form, 'election': election})


@login_required
@commissioner_only
def createControlVoteView(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    if request.method == 'POST':
        form = ControlVoteForm(request.POST)
        if form.is_valid():
            control_vote = form.save(commit=False)
            control_vote.election = election
            control_vote.save()
            messages.success(request, "Control vote added successfully.")
            return redirect('election_control_votes', pk=election_id)
    else:
        form = ControlVoteForm(initial={'election': election})
    return render(request, 'vote/create_control_vote.html', {'form': form, 'election': election})

@login_required
def dashboardView(request):
    # Initialize elections variable
    elections = []

    # Check the role of the logged-in user
    if request.user.profile.role == 'commissioner':
        # If the user is a commissioner, fetch all elections created by the commissioner
        elections = Election.objects.filter(commissioner=request.user)

    elif request.user.profile.role == 'voter':
        # If the user is a voter, fetch the voter object for the user
        voter = Voter.objects.filter(user=request.user).first()
        # If the voter object exists, fetch the elections the voter is associated with
        if voter:
            elections = Election.objects.filter(voters=voter.election)

    else:
        # For any other role, fetch all elections
        elections = Election.objects.all()

    # Render the dashboard template with the elections data
    return render(request, 'vote/dashboard.html', {'elections': elections})





from django.core.exceptions import ObjectDoesNotExist

@login_required
def dashboardView(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        # Create profile if it doesn't exist
        profile = Profile.objects.create(user=request.user)

    if profile.role == 'commissioner':
        elections = Election.objects.filter(commissioner=request.user)
    else:
        voter_ids = Voter.objects.filter(user=request.user).values_list('election', flat=True)
        elections = Election.objects.filter(id__in=voter_ids)

    return render(request, 'vote/dashboard.html', {'elections': elections})


@login_required
def resultView(request):
    elections = Election.objects.all()
    election_results = []

    for election in elections:
        candidates = Candidate.objects.filter(election=election).order_by('-total_vote')
        election_results.append({
            'election': election,
            'candidates': candidates
        })

    return render(request, 'vote/results.html', {
        'election_results': election_results
    })


@login_required
def electionDetailView(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)
    voter_id = request.session.get('voter_id')

    if request.method == 'POST':
        voter_id = request.POST.get('voter_id')
        try:
            if request.user.profile.role == 'commissioner':
                # Check if the user is the commissioner and if the provided voter_id matches their commissioner token
                if voter_id == election.commissioner_token:
                    request.session['voter_id'] = voter_id  # Save voter ID in session after validation
                else:
                    raise Voter.DoesNotExist  # Raise an exception if validation fails
            elif request.user.profile.role == 'voter':
                # Check if the voter ID matches the user's voter ID for this election
                voter = Voter.objects.get(voter_id=voter_id, election=election, user=request.user)
                request.session['voter_id'] = voter_id  # Save voter ID in session after validation
            else:
                raise Voter.DoesNotExist  # Raise an exception if the role is neither commissioner nor voter
        except Voter.DoesNotExist:
            messages.error(request, "Invalid Voter ID. You are not allowed to vote in this election.")
            return redirect('election_detail', election_id=election_id)

    if not voter_id:
        return render(request, 'vote/voter_id_prompt.html', {'election': election})

    # Prepare data for Chart.js
    candidate_names = [candidate.name for candidate in candidates]
    votes = [candidate.total_vote for candidate in candidates]
    total_voters_set = election.max_voters
    total_voters_with_id = election.voters.count()
    remaining_voters = total_voters_set - total_voters_with_id

    return render(request, 'vote/election_detail.html', {
        'election': election,
        'candidates': candidates,
        'candidate_names': candidate_names,
        'votes': votes,
        'has_ended': election.has_ended(),
        'total_voters_set': total_voters_set,
        'total_voters_with_id': total_voters_with_id,
        'remaining_voters': remaining_voters,
    })




@login_required
def voteCandidateView(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    election = candidate.election

        # Ensure the election has not ended
    if election.has_ended():
        messages.error(request, "The poll has closed. Voting is no longer allowed.")
        return redirect('election_detail', election_id=election.id)

    voter_id = request.POST.get('voter_id')

    # Ensure the user is a registered voter in this election
    try:
        voter = Voter.objects.get(user=request.user, election=election, voter_id=voter_id)
    except Voter.DoesNotExist:
        messages.error(request, "You are not allowed to vote in this election.")
        return redirect('election_detail', election_id=election.id)

    # Check if the user has already voted in this election for this position
    if ControlVote.objects.filter(user=request.user, election=election, position=candidate.position).exists():
        messages.error(request, "You have already voted for this position.")
        return redirect('election_detail', election_id=election.id)

    # Record the vote
    candidate.total_vote += 1
    candidate.save()

    # Mark the vote as cast
    ControlVote.objects.create(
        user=request.user,
        position=candidate.position,
        election=election,
        candidate=candidate,
        party=candidate.party,
        status=True
    )

    messages.success(request, "Your vote has been cast successfully.")
    return redirect('election_detail', election_id=election.id)

@login_required
def validateVoterId(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        voter_id = data.get('voter_id')
        election_id = data.get('election_id')
        election = get_object_or_404(Election, pk=election_id)
        try:
            Voter.objects.get(user=request.user, election=election, voter_id=voter_id)
            return JsonResponse({'is_valid': True})
        except Voter.DoesNotExist:
            return JsonResponse({'is_valid': False})
    return JsonResponse({'is_valid': False})


