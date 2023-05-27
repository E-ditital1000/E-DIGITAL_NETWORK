from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegistrationForm, ChangeForm
from .models import Candidate, Position, ControlVote
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
import os



def homeView(request):
    return render(request, "home.html")

def registrationView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['confirm_password']:
                national_id = cd['national_id']

                # Check if the national ID exists in the database and is not registered by another user
                if Profile.objects.filter(national_id=national_id, user__isnull=False).exists():
                    return render(request, "registration.html", {'form': form, 'note': 'This ID has already been used.'})

                # Validate the ID range
                start_id = 1000
                end_id = 2000
                entered_id = int(national_id.replace('ID', ''))
                if not (start_id <= entered_id <= end_id):
                    return render(request, "registration.html", {'form': form, 'note': 'Invalid ID. Please enter a valid ID within the specified range.'})

                user = form.save(commit=False)
                user.set_password(cd['password'])
                user.save()

                # Save additional profile fields
                profile = Profile.objects.create(user=user, district=cd['district'], county=cd['county'],
                                                 national_id=national_id, citizenship=cd['citizenship'],
                                                 age=cd['age'])
                messages.success(request, 'You have been registered.')
                return redirect('home')
            else:
                return render(request, "registration.html", {'form': form, 'note': 'Passwords must match.'})
    else:
        form = RegistrationForm()
    
    return render(request, "registration.html", {'form': form})




def dashboardView(request):
    # Get the total number of expected voters (e.g., from a database query)
    total_voters = 5000  # Replace with your actual logic to get the total number

    # Get the total number of registered voters (e.g., from a database query)
    registered_voters = Profile.objects.count()  # Replace with your actual logic to count the registered voters

    context = {
        'total_voters': total_voters,
        'registered_voters': registered_voters
    }

    return render(request, 'dashboard.html', context)

def loginView(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
            return render(request, "login.html")
    else:
        return render(request, "login.html")


@login_required
def logoutView(request):
    logout(request)
    return redirect('home')


@login_required
def dashboardView(request):
    return render(request, "dashboard.html")


@login_required
def positionView(request):
    obj = Position.objects.all()
    return render(request, "position.html", {'obj': obj})


@login_required
def candidateView(request, pos):
    obj = get_object_or_404(Position, pk=pos)
    if request.method == "POST":

        temp = ControlVote.objects.get_or_create(
            user=request.user, position=obj)[0]

        if temp.status == False:
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/position/')
        else:
            messages.success(
                request, 'you have already been voted this position.')
            return render(request, 'candidate.html', {'obj': obj})
    else:
        return render(request, 'candidate.html', {'obj': obj})


@login_required
def resultView(request):
    obj = Candidate.objects.all().order_by('position', '-total_vote')
    return render(request, "result.html", {'obj': obj})


@login_required
def candidateDetailView(request, id):
    obj = get_object_or_404(Candidate, pk=id)
    return render(request, "candidate_detail.html", {'obj': obj})


@login_required
def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "password.html", {'form': form})


@login_required
def editProfileView(request):
    if request.method == "POST":
        form = ChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ChangeForm(instance=request.user)
    return render(request, "edit_profile.html", {'form': form})
