#!/usr/bin/python

import requests
import bs4

class Club:
	"""A MLS Club"""
	def __init__(self, name, abbreviation, subreddit):
		self.name = name
		self.abbreviation = abbreviation
		self.subreddit = subreddit

CHI = Club('Chicago Fire', 'CHI', '/r/chicagofire')
COL = Club('Colorado Rapids', 'COL', '/r/rapids')
CLB = Club('Columbus Crew SC', 'CLB', '/r/thremassive')
DC = Club('D.C. United', 'DC', '/r/dcunited')
FCD = Club('FC Dallas', 'DAL', '/r/fcdallas')
HOU = Club('Houston Dynamo', 'HOU', '/r/dynamo')
LAG = Club('LA Galaxy', 'LA', '/r/lagalaxy')
MTL = Club('Montreal Impact', 'MTL', '/r/montrealimpact')
NE = Club('New England Revolution', 'NE', '/r/newenglandrevolution')
NYC = Club('New York City FC', 'NYC', '/r/nycfc')
NYRB = Club('New York Red Bulls', 'NYRB', '/r/rbny')
OCSC = Club('Orlando City SC', 'OCSC', '/r/oclions')
PHI = Club('Philadelphia Union', 'PHI', '/r/phillyunion')
POR = Club('Portland Timbers', 'POR', '/r/timbers')
RSL = Club('Real Salt Lake', 'RSL', '/r/realsaltlake')
SJ = Club('San Jose Earthquakes', 'SJ', '/r/sjearthquakes')
SEA = Club('Seattle Sounders FC', 'SEA', '/r/soundersfc')
SKC = Club('Sporting Kansas City', 'SKC', '/r/sportingkc')
TOR = Club('Toronto FC', 'TFC', '/r/tfc')
VAN = Club('Vancouver Whitecaps FC', 'VAN', '/r/whitecapsfc')

ALL_CLUBS = {
	CHI, COL, CLB, DC, FCD, HOU, LAG, MTL, NE, NYC, NYRB, OCSC, PHI, POR, RSL,
	SJ, SEA, SKC, TOR, VAN
}

# Setup our variables for URLs and data to parse
standings_url = requests.get('http://www.mlssoccer.com/standings')
standing_soup = bs4.BeautifulSoup(standings_url.text)

# Western Conference is the 2nd table
standings = standing_soup.select('.stats-table')[1]
standings_data = standings.find('tbody').find_all('tr')

def strip_text(text):
	return text.get_text().strip();

def link_club(_club):
	abbr = all_clubs[_club][0]
	sub = all_clubs[_club][1]
	club = '[%s](%s)' % (abbr, sub)
	return club

def format_club(_club):
	club = strip_text(_club)
	club = link_club(club)
	return club

# Print the standings to stdout
for row in standings_data:
	cells = row.find_all('td')
	rank = strip_text(cells[0])
	club = format_club(cells[1].find('a')) # find 'a' to ignore playoff indicator
	points = '**%s**' % strip_text(cells[2])
	gp = strip_text(cells[3])
	gd = strip_text(cells[10])
	gf = strip_text(cells[8])
	print '%s|%s|%s|%s|%s|%s' % (rank, club, points, gp, gd, gf)
