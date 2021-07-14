from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save


class Group(models.Model):
	title = models.CharField(max_length=20, verbose_name="Naziv")

	class Meta:
		ordering = ["pk"]
		verbose_name = "Grupa"
		verbose_name_plural = "Grupe"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("group_details", kwargs={"pk": self.pk})

	@property
	def fields(self):
		fields = []
		for f in self._meta.fields[1:]:
			fields.append({"name": f.verbose_name, "value": f.value_to_string(self)})
		return fields

	@property
	def first_field(self):
		return self.fields[0]["value"]


class Team(models.Model):
	name = models.CharField(max_length=50, verbose_name="Tim")
	description = models.TextField(null=True, blank=True, verbose_name="Opis")
	group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="teams", verbose_name="Grupa")
	# thumbnail = models.ImageField(null=True, blank=True, upload_to="images/teams/", verbose_name="Sličica")
	wins = models.IntegerField(null=True, blank=True, verbose_name="Pobede", help_text="Koliko pobeda je tim imao?", default=0)
	draws = models.IntegerField(null=True, blank=True, verbose_name="Remiji", help_text="Koliko puta je tim odigrao nerešen meč?", default=0)
	loses = models.IntegerField(null=True, blank=True, verbose_name="Porazi", help_text="Koliko poraza je tim imao?", default=0)
	goals_scored = models.IntegerField(verbose_name="Postignuti golovi", help_text="Koliko golova je tim postigao?", default=0)
	goals_received = models.IntegerField(verbose_name="Primljeni golovi", help_text="Koliko golova je tim primio?", default=0)
	points = models.IntegerField(verbose_name="Bodovi", help_text="Koliko tim ima bodova?", default=0)

	class Meta:
		ordering = ["group", "-points", "-goals_scored", "goals_received", "name"]
		verbose_name = "Tim"
		verbose_name_plural = "Timovi"

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("team_details", kwargs={"pk": self.pk})

	@property
	def matches_played(self):
		return self.matches_hosted.count() + self.matches_away.count()
	matches_played.fget.short_description = "Odigrano"

	@property
	def goal_difference(self):
		return self.goals_scored - self.goals_received
	goal_difference.fget.short_description = "Gol razlika"

	@property
	def fields(self):
		fields = []
		for f in self._meta.fields[1:]:
			if f.name == "group":
				fields.append({"name": f.verbose_name, "value": self.group.title})
			else:
				fields.append({"name": f.verbose_name, "value": f.value_to_string(self)})
		fields.insert(3, {"name": "Odigrano", "value": self.matches_played})
		fields.insert(-1, {"name": "Gol razlika", "value": self.goal_difference})
		return fields

	@property
	def first_field(self):
		return self.fields[0]["value"]


class Phase(models.Model):
	title = models.CharField(max_length=20, verbose_name="Naziv")
	description = models.TextField(null=True, blank=True, verbose_name="Opis")

	class Meta:
		verbose_name = "Faza takmičenja"
		verbose_name_plural = "Faze takmičenja"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("phase_details", kwargs={"pk": self.pk})

	@property
	def matches_played(self):
		return self.matches.count()
	matches_played.fget.short_description = "Odigrano"

	@property
	def fields(self):
		fields = []
		for f in self._meta.fields[1:]:
			fields.append({"name": f.verbose_name, "value": f.value_to_string(self)})
		fields.append({"name": "Odigrano", "value": self.matches_played})
		return fields

	@property
	def first_field(self):
		return self.fields[0]["value"]


class Match(models.Model):
	title = models.CharField(max_length=100, verbose_name="Naslov")
	overview = models.TextField(null=True, blank=True, verbose_name="Sažetak")
	date = models.DateField(verbose_name="Datum", help_text="Kada je odigran meč?")
	phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name="matches", verbose_name="Faza takmičenja")
	team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matches_hosted", verbose_name="Tim 1")
	team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matches_away", verbose_name="Tim 2")
	team1_goals = models.IntegerField(verbose_name="Golovi tima 1", help_text="Koliko golova je postigao tim 1?")
	team2_goals = models.IntegerField(verbose_name="Golovi tima 2", help_text="Koliko golova je postigao tim 2?")
	stadium = models.CharField(max_length=200, verbose_name="Stadion", help_text="Na kom stadionu je igran meč?")
	spectators = models.IntegerField(verbose_name="Gledaoci", help_text="Koliko je ljudi bilo na tribinama?")
	referee = models.CharField(max_length=100, verbose_name="Sudija", help_text="Ko je bio glavni sudija na ovom meču?")
	previous_match = models.ForeignKey("self", related_name="previous", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Prethodni meč")
	next_match = models.ForeignKey("self", related_name="next", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sledeći meč")
	# thumbnail = models.ImageField(null=True, blank=True, upload_to="images/matches/", verbose_name="Sličica")

	class Meta:
		verbose_name = "Meč"
		verbose_name_plural = "Mečevi"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("match_details", kwargs={"pk": self.pk})

	@property
	def fields(self):
		fields = []
		for f in self._meta.fields[1:]:
			if f.name == "phase":
				fields.insert(0, {"name": f.verbose_name, "value": self.phase.title})
			elif f.name == "team1":
				fields.append({"name": f.verbose_name, "value": self.team1.name})
			elif f.name == "team2":
				fields.append({"name": f.verbose_name, "value": self.team2.name})
			elif f.name == "previous_match":
				fields.append({"name": f.verbose_name, "value": self.previous_match.title})
			elif f.name == "next_match":
				fields.append({"name": f.verbose_name, "value": self.next_match.title})
			else:
				fields.append({"name": f.verbose_name, "value": f.value_to_string(self)})
		print(fields)
		return fields

	@property
	def first_field(self):
		return self.fields[0]["value"]


@receiver(post_save, sender=Match)
def match_saved(sender, instance, **kwargs):
	if kwargs["created"]:
		team1 = instance.team1
		team2 = instance.team2
		t1_goals = instance.team1_goals
		t2_goals = instance.team2_goals
		if t1_goals > t2_goals: # team 1 won
			team1.wins = team1.wins + 1
			team1.points = team1.points + 3
			team2.loses = instance.team2.loses + 1
		elif t1_goals < t2_goals: # team 1 lost
			team2.wins = team2.wins + 1
			team2.points = team2.points + 3
			team1.loses = team1.loses + 1
		else: # a draw
			team1.draws = team1.draws + 1
			team1.points = team1.points + 1
			team2.draws = team2.draws + 1
			team2.points = team2.points + 1
		team1.goals_scored = team1.goals_scored + t1_goals
		team1.goals_received = team1.goals_received + t2_goals
		team2.goals_scored = team2.goals_scored + t2_goals
		team2.goals_received = team2.goals_received + t1_goals
		team1.save()
		team2.save()
