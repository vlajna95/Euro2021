from django.contrib import admin
from .models import Group, Team, Phase, Match


class CustomModelAdmin(admin.ModelAdmin):
	def __init__(self, model, admin_site):
		self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
		super(CustomModelAdmin, self).__init__(model, admin_site)


# inlines

class TeamsInline(admin.TabularInline):
	model = Team
	extra = 0

class MatchesInline(admin.StackedInline):
	model = Match


# model admins

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	model = Group
	inlines = [TeamsInline]
	list_filter = ["title"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	model = Team
	list_display = ["name", "description", "group", "matches_played", "wins", "draws", "loses", "goals_scored", "goals_received", "goal_difference", "points"]
	list_filter = ["group"]
	search_fields = ["name"]


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
	model = Phase


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
	model = Match
	list_display = ["title", "overview", "phase", "team1", "team2", "team1_goals", "team2_goals", "referee", "stadium", "spectators", "previous_match", "next_match"]
	list_filter = ["phase", "team1", "team2", "stadium", "referee"]
	search_fields = ["title", "overview", "team1", "team2"]
