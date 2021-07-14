import graphene
from graphene_django import DjangoObjectType
from matches.models import *


class GroupType(DjangoObjectType):
	class Meta:
		model = Group


class TeamType(DjangoObjectType):
	class Meta:
		model = Team


class PhaseType(DjangoObjectType):
	class Meta:
		model = Phase


class MatchType(DjangoObjectType):
	class Meta:
		model = Match


class Query(graphene.ObjectType):
	all_matches = graphene.List(MatchType)
	match_by_title = graphene.Field(MatchType, title=graphene.String())
	matches_by_phase = graphene.List(MatchType, phase=graphene.String())
	all_teams = graphene.List(TeamType)
	team_by_name = graphene.Field(TeamType, name=graphene.String())
	teams_by_group = graphene.List(TeamType, group=graphene.String())

	def resolve_all_matches(root, info):
		return (Match.objects.select_related("phase", "team1", "team2", "previous_match", "next_match").all())

	def resolve_match_by_title(root, info, title):
		return Match.objects.select_related("phase", "team1", "team2", "previous_match", "next_match").get(title=title)

	def resolve_matches_by_phase(root, info, phase):
		return (Match.objects.select_related("phase", "team1", "team2", "previous_match", "next_match").filter(phase__title__iexact=phase))

	def resolve_all_teams(root, info):
		return (Team.select_related("group").objects.all())

	def resolve_team_by_name(root, info, name):
		return Team.objects.select_related("group").get(name=name)

	def resolve_teams_by_group(root, info, group):
		return (Team.objects.select_related("group").filter(group__title__iexact=group))


schema = graphene.Schema(query=Query)
