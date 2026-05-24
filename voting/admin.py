from django.contrib import admin
from .models import Election, Candidate, Vote

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 3

class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active', 'total_votes')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    inlines = [CandidateInline]

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'election', 'party_name', 'vote_count')
    list_filter = ('election',)
    search_fields = ('name', 'party_name')

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'election', 'candidate', 'timestamp')
    list_filter = ('election', 'candidate')
    search_fields = ('user__username', 'election__title', 'candidate__name')
    readonly_fields = ('timestamp',)

admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Vote, VoteAdmin)
