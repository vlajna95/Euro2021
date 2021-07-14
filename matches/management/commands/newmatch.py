from django.core.management.base import BaseCommand, CommandError
import pyperclip as clip


class Command(BaseCommand):
	help = "Creates a text document with a template for the description of a match"

	def add_arguments(self, parser):
		parser.add_argument("match_name", type=str)

	def handle(self, *args, **options):
		template = ""
		open_section = "<section>\n"
		open_header = "<header>\n"
		open_h2 = "<h2>"
		open_h3 = "<h3>"
		close_section = "</section>\n"
		close_header = "</header>\n"
		close_h2 = "</h2>\n"
		close_h3 = "</h3>\n"
		description_paragraph = "<p></p><br />\n"
		halftime_score = "<p>Rezultat na poluvremenu: </p>\n"
		scorers_section = open_section + open_header + open_h2 + "Strelci" + close_h2 + close_header + "<ul>\n\n</ul>\n" + close_section
		players1 = "<ul>\n" + str.join("", [f"<li>{name}</li>\n" for name in clip.paste().splitlines()[:11]]) + "</ul>\n"
		players2 = "<ul>\n" + str.join("", [f"<li>{name}</li>\n" for name in clip.paste().splitlines()[11:]]) + "</ul>\n"
		lineup1_section = open_section + open_header + open_h3 + "Reprezentacija 1" + close_h3 + "Trener: \n" + close_header + players1 + close_section
		lineup2_section = open_section + open_header + open_h3 + "Reprezentacija 2" + close_h3 + "Trener: \n" + close_header + players2 + close_section
		lineups_section = open_section + open_header + open_h2 + "Postave" + close_h2 + close_header + lineup1_section + lineup2_section + close_section
		template = open_section + description_paragraph + halftime_score + close_section + "\n" + scorers_section + "\n" + lineups_section
		with open(options["match_name"] + ".txt", "w", encoding="utf-8") as f:
			f.write(template)
