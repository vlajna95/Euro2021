from django.urls import path
from .views import SearchMatches, MatchList, MatchDetails, PhaseList, PhaseDetails, TeamList, TeamDetails, GroupList, GroupDetails

urlpatterns = [
	path("search_matches/", SearchMatches.as_view(), name="search_matches"),
	path("", MatchList.as_view(), name="match_list"),
	path("match/<pk>", MatchDetails.as_view(), name="match_details"),
	path("phases/", PhaseList.as_view(), name="phase_list"),
	path("phase/<pk>", PhaseDetails.as_view(), name="phase_details"),
	path("teams/", TeamList.as_view(), name="team_list"),
	path("team/<pk>", TeamDetails.as_view(), name="team_details"),
	path("groups/", GroupList.as_view(), name="group_list"),
	path("group/<pk>", GroupDetails.as_view(), name="group_details"),
]
