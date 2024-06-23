"""
URL configuration for Evote project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dal import autocomplete
from vote import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homeView, name='home'),
    path('register/', views.registrationView, name='register'),
    path('login/', views.loginView, name='login'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('logout/', views.logoutView, name='logout'),
    path('position/', views.positionView, name='position'),
    path('candidate/<int:pos>/', views.candidateView, name='candidate'),
    path('candidate/detail/<int:id>/', views.candidateDetailView, name='detail'),
    path('result/', views.resultView, name='result'),
    path('changepass/', views.changePasswordView, name='changepass'),
    path('editprofile/', views.editProfileView, name='editprofile'),
    path('create-election/', views.createElectionView, name='create_election'),
    path('register-voter/<int:election_id>/', views.registerVoterView, name='register_voter'),
    path('election/<int:election_id>/', views.electionDetailView, name='election_detail'),
    path('election/<int:election_id>/create-candidate/', views.createCandidateView, name='create_candidate'),
    path('create-control-vote/<int:election_id>/', views.createControlVoteView, name='create_control_vote'),
    path('vote-candidate/<int:candidate_id>/', views.voteCandidateView, name='vote_candidate'),  # Add this line
    path('validate_voter/', views.validateVoterId, name='validate_voter'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('user-autocomplete/', autocomplete.Select2ListView.as_view(), name='user-autocomplete'),
    
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)


    