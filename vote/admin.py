from django.contrib import admin
from .models import Candidate, Position, Election, Profile, Voter, Observer, ControlVote, Notification

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'election', 'party', 'total_vote')
    list_filter = ('position', 'election', 'party')
    search_fields = ('name', 'position__title', 'election__name')
    readonly_fields = ('total_vote',)

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'commissioner', 'start_time', 'end_time', 'max_voters', 'max_observers')
    search_fields = ('name', 'commissioner__username')
    list_filter = ('start_time', 'end_time')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_read', 'created_at', 'election')
    search_fields = ('message',)
    list_filter = ('is_read', 'created_at', 'election')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'district', 'county', 'citizenship', 'age', 'role')
    search_fields = ('user__username', 'district', 'county')
    list_filter = ('district', 'county', 'citizenship', 'role')

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('user', 'election', 'voter_id')
    search_fields = ('user__username', 'election__name', 'voter_id')
    list_filter = ('election',)

@admin.register(Observer)
class ObserverAdmin(admin.ModelAdmin):
    list_display = ('user', 'election', 'observer_id')
    search_fields = ('user__username', 'election__name', 'observer_id')
    list_filter = ('election',)

@admin.register(ControlVote)
class ControlVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'election', 'party', 'status')
    search_fields = ('user__username', 'position__title', 'election__name', 'party')
    list_filter = ('status', 'party')
