
from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q,Count

from . import team_maker
import leagues

def index(request):
	# 	all teams in the Atlantic Soccer Conference
	atlanticTeams = League.objects.get(name='Atlantic Soccer Conference')
	atlanticTeams = atlanticTeams.teams.all()

	# all (current) players on the Boston Penguins
	bostonPenguinsplayers = Team.objects.get(team_name='Penguins', location='Boston').curr_players.all()

	# all (current) players in the International Collegiate Baseball Conference
	InterCollegiate = League.objects.get(name='International Collegiate Baseball Conference').teams.all()
	
	InterCollegiatePlayers = []
	for team in InterCollegiate:
		for player in team.curr_players.all():
			InterCollegiatePlayers.append(player)
	
	# all (current) players in the American Conference of Amateur Football with last name "Lopez"
	amateurTeams = League.objects.get(name='American Conference of Amateur Football').teams.all()
	
	amateurTeamsPlayers = []
	for team in amateurTeams:
		for player in team.curr_players.all():
			if player.last_name == "Lopez":
				amateurTeamsPlayers.append(player)

	# all football players
	footballLeagues = League.objects.filter(name__contains = 'Football')
	footballTeamsPlayers = []
	for league1 in footballLeagues:
		for team in league1.teams.all():
			for player in team.all_players.all():
				footballTeamsPlayers.append(player)

	# all teams with a (current) player named "Sophia"
	sophias = Player.objects.filter(first_name = 'Sophia')
	sophiasTeams = []
	for sophie in sophias:
		sophiasTeams.append(sophie.curr_team)
	# all leagues with a (current) player named "Sophia"
	sophialeagues = {}
	for team in sophiasTeams:
		if not(sophialeagues.get(team.league.name)):
			sophialeagues[team.league.name]= team.league

	# everyone with the last name "Flores" who DOESN'T (currently) play for the Washington Roughriders
	floreses = Player.objects.filter(last_name = 'Flores')
	floresesExclude = []
	for flores in floreses:
		if not (flores.curr_team.team_name== 'Roughriders' and flores.curr_team.location == 'Washington') : floresesExclude.append(flores)
	
	# all teams, past and present, that Samuel Evans has played with
	Samuel = Player.objects.get(first_name='Samuel',last_name='Evans').all_teams.all()

	# all players, past and present, with the Manitoba Tiger-Cats
	Tiger_Cats = Team.objects.get(team_name='Tiger-Cats',location='Manitoba')
	Tiger_CatsPlayers = Tiger_Cats.all_players.all()

	# all players who were formerly (but aren't currently) with the Wichita Vikings
	vikings = Team.objects.get(team_name='Vikings',location='Wichita').all_players.all()
	vikingsCurrent = Team.objects.get(team_name='Vikings',location='Wichita').curr_players.all()

	vikingsPlayers = []
	flag = True
	for player in vikings:
		for player2 in vikingsCurrent:
			if player2.first_name == player.first_name and player2.last_name == player.last_name:
				flag = False
				break
		if (flag):
			vikingsPlayers.append(player)
			flag = True

	# every team that Jacob Gray played for before he joined the Oregon Colts
	jacob = Player.objects.get(first_name='Jacob',last_name='Gray')
	jacobTeams = jacob.all_teams.exclude(team_name='Colts',location='Oregon')

	# everyone named "Joshua" who has ever played in the Atlantic Federation of Amateur Baseball Players
	atlanticLeagueTeams = League.objects.get(name='Atlantic Federation of Amateur Baseball Players').teams.all()
	joshuas = []
	for team in atlanticLeagueTeams:
		for player in team.all_players.all():
			if player.first_name == "Joshua":
				joshuas.append(player)

	print("---" * 50)
	print(joshuas)

	# all teams that have had 12 or more players, past and present. (HINT: Look up the Django annotate function.)
	#without annotate
	teams12 = []
	for team in Team.objects.all():
		if len(team.all_players.all())>= 12:
			teams12.append(team)
	
	teams12ormore = []
	#using annotate
	team12count = Team.objects.all().annotate(Count('all_players'))
	for team in team12count:
		if team.all_players__count >=12:
			teams12ormore.append(team)

	# all players and count of teams played for, sorted by the number of teams they've played for
	countTeams = Player.objects.all().annotate(Count('all_teams')).order_by('all_teams__count')
	print("---" * 50)
	print(vars(countTeams[0]))
	context = {
		'countTeams':countTeams,
		'teams12ormore':teams12ormore,
		'teams12':teams12,
		'joshuas':joshuas,
		'jacobTeams':jacobTeams,
		'vikingsPlayers':vikingsPlayers,
		'Tiger_CatsPlayers':Tiger_CatsPlayers,
		'Samuel':Samuel,
		'floresesExclude':floresesExclude,
		'sophialeagues':sophialeagues,
		'sophiasTeams':sophiasTeams,
		'footballTeamsPlayers':footballTeamsPlayers,
		'amateurTeamsPlayers':amateurTeamsPlayers,
		'InterCollegiatePlayers':InterCollegiatePlayers,
		'bostonPenguinsplayers':bostonPenguinsplayers,
		'atlanticTeams': atlanticTeams,
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