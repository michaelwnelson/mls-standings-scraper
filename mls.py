#!/usr/bin/python
import sys
import requests
import bs4

class Club:
	"""A MLS Club

	Required Attributes:
		name: The name of the club.
		abbreviation: The common abbreviation for the club.
		subreddit: The subreddit (per /r/mls) for the club.
	Optional Attributes:
		points: Total accumulated points.
		games_played: Number of games played.
		goal_difference: The positive or negative goal difference. This is
			the sum of goals for and goals against.
		goals_for: Total number of goals scored.
	"""

	def __init__(self, name, abbreviation, conference, subreddit, rank=0,
				points=0, games_played=0, goal_difference=0, goals_for=0):
		self.name = name
		self.abbreviation = abbreviation
		self.conference = conference
		self.subreddit = subreddit
		self.rank = rank
		self.points = points
		self.games_played = games_played
		self.goal_difference = goal_difference
		self.goals_for = goals_for

	def __str__(self):
		return '%s|[%s](%s)|**%s**|%s|%s|%s' % (self.rank, self.abbreviation,
			self.subreddit, self.points, self.games_played,
			self.goal_difference, self.goals_for)

CHI  = Club('Chicago Fire',           'CHI',  'Eastern', '/r/chicagofire')
COL  = Club('Colorado Rapids',        'COL',  'Western', '/r/rapids')
CLB  = Club('Columbus Crew SC',       'CLB',  'Eastern', '/r/thremassive')
DC   = Club('D.C. United',            'DC',   'Eastern', '/r/dcunited')
FCD  = Club('FC Dallas',              'DAL',  'Western', '/r/fcdallas')
HOU  = Club('Houston Dynamo',         'HOU',  'Western', '/r/dynamo')
LAG  = Club('LA Galaxy',              'LA',   'Western', '/r/lagalaxy')
MTL  = Club('Montreal Impact',        'MTL',  'Eastern', '/r/montrealimpact')
NE   = Club('New England Revolution', 'NE',   'Eastern', '/r/newenglandrevolution')
NYC  = Club('New York City FC',       'NYC',  'Eastern', '/r/nycfc')
NYRB = Club('New York Red Bulls',     'NYRB', 'Eastern', '/r/rbny')
OCSC = Club('Orlando City SC',        'OCSC', 'Eastern', '/r/oclions')
PHI  = Club('Philadelphia Union',     'PHI',  'Eastern', '/r/phillyunion')
POR  = Club('Portland Timbers',       'POR',  'Western', '/r/timbers')
RSL  = Club('Real Salt Lake',         'RSL',  'Western', '/r/realsaltlake')
SJ   = Club('San Jose Earthquakes',   'SJ',   'Western', '/r/sjearthquakes')
SEA  = Club('Seattle Sounders FC',    'SEA',  'Western', '/r/soundersfc')
SKC  = Club('Sporting Kansas City',   'SKC',  'Western', '/r/sportingkc')
TOR  = Club('Toronto FC',             'TFC',  'Eastern', '/r/tfc')
VAN  = Club('Vancouver Whitecaps FC', 'VAN',  'Western', '/r/whitecapsfc')

ALL_CLUBS = {
	CHI, COL, CLB, DC, FCD, HOU, LAG, MTL, NE, NYC, NYRB, OCSC, PHI, POR, RSL,
	SJ, SEA, SKC, TOR, VAN
}

def strip_text(text):
	return text.get_text().strip();

def find_club(name):
	for club in ALL_CLUBS:
		# playoffs really mess this up
		if name.startswith(("x", "y", "s")):
			name = name[4:]
		if club.name.lower() == name.lower():
			return club

	sys.exit("Could not find club %s" % name)

def setup(data):
	for row in data:
		cells = row.find_all('td')
		rank = strip_text(cells[0])
		# skip first row of tables as it's a psuedo table header
		if rank == "#":
			continue
		name = strip_text(cells[1])
		points = strip_text(cells[2])
		gp = strip_text(cells[5])
		gd = strip_text(cells[11])
		gf = strip_text(cells[9])
		# Set Club's option attributes
		club = find_club(name)
		club.rank = rank
		club.points = points
		club.games_played = gp
		club.goal_difference = gd
		club.goals_for = gf

def standings(conference):
	clubs = sorted(ALL_CLUBS, key=lambda c: int(c.rank))
	print "Pos|Club|Pts|GP|GD|GF"
	print ":--:|:--|:--:|:--:|:--:|:--:"
	for club in clubs:
		if club.conference.lower() == conference.lower():
			print club

def main():
	# Setup our variables for URLs and data to parse
	standings_url = requests.get('http://www.mlssoccer.com/standings')
	standing_soup = bs4.BeautifulSoup(standings_url.text)

	# East Conference is the 1st table
	eastern_table = standing_soup.select('.standings_table')[0]
	eastern_data = eastern_table.find('tbody').find_all('tr')

	# Western Conference is the 2nd table
	western_table = standing_soup.select('.standings_table')[1]
	western_data = western_table.find('tbody').find_all('tr')

	all_data = eastern_data + western_data
	setup(all_data)
	print "=== Eastern Conference ==="
	standings("Eastern")
	print "\n=== Western Conference ==="
	standings("Western")

if __name__ == '__main__':
	main()
