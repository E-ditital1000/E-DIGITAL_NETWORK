from django.contrib import admin
from .models import Candidate, Position, Election, Profile, Voter, ControlVote

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
    list_display = ('name', 'commissioner', 'start_time', 'end_time', 'max_voters')
    search_fields = ('name', 'commissioner__username')
    list_filter = ('start_time', 'end_time')

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

@admin.register(ControlVote)
class ControlVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'election', 'party', 'status')
    search_fields = ('user__username', 'position__title', 'election__name', 'party')
    list_filter = ('status', 'party')
