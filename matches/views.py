from django.views.generic import View, ListView, DetailView
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from .models import Group, Team, Phase, Match


def get_phase_count():
	queryset = Match.objects.values("phase__title").annotate(Count("phase__title"))
	return queryset

latest_matches = Match.objects.order_by("-pk")[:5]


class SearchMatches(View):
	def get(self, request, *args, **kwargs):
		queryset = Match.objects.all()
		query = request.GET.get("q")
		if query:
			queryset = queryset.filter(Q(title__icontains=query) | Q(overview__icontains=query)).distinct()
		context = {"queryset": queryset, "most_recent": Match.objects.order_by("-pk")[:5]}
		return render(request, "matches/search_results.html", context)


class MatchList(ListView):
	model = Match
	template_name = "matches/matches.html"
	queryset = Match.objects.order_by("-pk")
	context_object_name = "queryset"
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["page_request_var"] = "page"
		context["most_recent"] = latest_matches
		return context


class MatchDetails(DetailView):
	model = Match
	template_name = "matches/match.html"
	context_object_name = "match"

	def get_object(self):
		obj = super().get_object()
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["most_recent"] = latest_matches
		return context


class PhaseList(ListView):
	model = Phase
	template_name = "matches/phases.html"
	context_object_name = "queryset"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["most_recent"] = latest_matches
		return context


class PhaseDetails(DetailView):
	model = Phase
	template_name = "matches/phase.html"
	context_object_name = "phase"

	def get_object(self):
		obj = super().get_object()
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["most_recent"] = latest_matches
		return context


class TeamList(ListView):
	model = Team
	template_name = "matches/detailed_listing.html"
	context_object_name = "queryset"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["page_title"] = "Timovi"
		context["most_recent"] = latest_matches
		return context


class TeamDetails(DetailView):
	model = Team
	template_name = "matches/team.html"
	context_object_name = "team"

	def get_object(self):
		obj = super().get_object()
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["most_recent"] = latest_matches
		return context


class GroupList(ListView):
	model = Group
	template_name = "matches/groups.html"
	context_object_name = "queryset"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["most_recent"] = latest_matches
		return context


class GroupDetails(DetailView):
	model = Group
	template_name = "matches/group.html"
	context_object_name = "group"

	def get_object(self):
		obj = super().get_object()
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["most_recent"] = latest_matches
		return context
