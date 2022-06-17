from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q


from . import team_maker
import leagues

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
	}
	return render(request, "leagues/index.html", context)

def update(request):

	baseballLeagues = League.objects.all().filter(sport='Baseball')
	
	womenLeaguese = League.objects.filter(name__contains='women')

	# all leagues where sport is any type of hockey
	hockeyLeagues = League.objects.filter(sport__contains='Hockey')

	#all leagues where sport is something OTHER THAN football
	noFootball = League.objects.exclude(sport='Football')

	#all leagues that call themselves "conferences"
	conferences = League.objects.filter(name__contains='Conference')

	#all leagues in the Atlantic region
	atlanticLeagues = League.objects.filter(name__contains='Atlantic')

	# all teams based in Dallas
	dallasTeams = Team.objects.filter(location='Dallas')
	#all teams named the Raptors
	raptorsTeams = Team.objects.filter(team_name='Raptors')
	#all teams whose location includes "City"
	cityTeams = Team.objects.filter(location__contains = 'City')
	#all teams whose names begin with "T"
	tTeams = Team.objects.filter(team_name__startswith = 'T')
	#all teams, ordered alphabetically by location
	teamsbyLoc = Team.objects.order_by('location')
	#all teams, ordered by team name in reverse alphabetical order
	teamsby_name = Team.objects.order_by('-team_name')

	#every player with last name "Cooper"
	coopers = Player.objects.filter(last_name="Cooper")

	# every player with first name "Joshua"
	Joshuas = Player.objects.filter(first_name="Joshua")

	#every player with last name "Cooper" EXCEPT those with "Joshua" as the first name
	coopers2 = Player.objects.exclude(first_name="Joshua").filter(last_name="Cooper")

	#all players with first name "Alexander" OR first name "Wyatt"
	alexanderORWyatt = Player.objects.filter(Q(first_name="Alexander"))| Player.objects.filter(Q(first_name='Wyatt'))

	context = {
		'alexanderORWyatt':alexanderORWyatt,
		'coopers2':coopers2,
		'Joshuas':Joshuas,
		'coopers':coopers,
		'teamsby_name':teamsby_name,
		'teamsbyLoc':teamsbyLoc,
		'tTeams': tTeams,
		'cityTeams': cityTeams,
		'raptorsTeams': raptorsTeams,
		'dallasTeams':dallasTeams,
		'atlanticLeagues':atlanticLeagues,
		'conferences' : conferences,
		'noFootball': noFootball,
		'hockeyLeagues': hockeyLeagues,
		'baseballLeagues' : baseballLeagues,
		'womenLeaguese' : womenLeaguese,
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
	}
	return render(request, "leagues/updated.html", context)


def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)
	print('--'*50)
	print('done')
	return redirect("index")